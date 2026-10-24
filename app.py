from __future__ import annotations
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

st.set_page_config(page_title="Client Intelligence Lab", page_icon="◈", layout="wide")
st.markdown("""<style>.block-container{max-width:1500px;padding-top:1.4rem} h1,h2{letter-spacing:-.03em} [data-testid=stMetric]{border:1px solid #e4e7eb;padding:14px;border-radius:12px}</style>""",unsafe_allow_html=True)
st.title("Client Intelligence Lab")
st.caption("Corporate & Institutional Banking · independent portfolio prototype · synthetic data")
st.warning("Educational demonstration only. Not affiliated with HSBC and not based on HSBC data. No real client decisions should be made from this app.")

@st.cache_data
def build_data(n=1200, seed=41):
    rng=np.random.default_rng(seed)
    sectors=np.array(["Technology","Industrials","Healthcare","Energy","Consumer","Financial Services","Materials"])
    regions=np.array(["UK & Europe","North America","Asia Pacific","Middle East"])
    sector=rng.choice(sectors,n); region=rng.choice(regions,n)
    revenue=np.clip(rng.lognormal(5.2,.9,n),5,1500)
    tenure=rng.integers(1,31,n); products=rng.integers(1,8,n)
    digital=np.clip(rng.beta(2.2,2,n),0,1); engagement=np.clip(rng.beta(2,2,n),0,1)
    leverage=np.clip(rng.normal(.42,.2,n),.02,1.4)
    sector_effect=pd.Series(sector).map({"Technology":.35,"Industrials":.1,"Healthcare":.15,"Energy":.0,"Consumer":-.1,"Financial Services":.2,"Materials":-.05}).to_numpy()
    logit=-1.5+.0009*revenue+.65*digital+.6*engagement+.13*products-.025*tenure+sector_effect
    prob=1/(1+np.exp(-logit)); adopted=rng.binomial(1,prob)
    wallet=np.clip(revenue*rng.uniform(.015,.12,n)*(1+.3*engagement),.1,120)
    treatment=rng.binomial(1,.5,n); outcome=adopted+rng.binomial(1,np.clip(.03+.08*treatment,0,.3),n)
    df=pd.DataFrame({"client_id":[f"SYN-{i+1:05d}" for i in range(n)],"sector":sector,"region":region,"annual_revenue_usd_m":revenue.round(2),"relationship_tenure_years":tenure,"products_held":products,"digital_activity_score":digital.round(3),"engagement_score":engagement.round(3),"leverage_proxy":leverage.round(3),"adopted_simulated":adopted,"estimated_wallet_gap_usd_m":wallet.round(2),"treatment_assignment":treatment,"simulated_campaign_outcome":outcome})
    return df

def score(df):
    features=["annual_revenue_usd_m","relationship_tenure_years","products_held","digital_activity_score","engagement_score","leverage_proxy","sector","region"]
    cat=["sector","region"]; num=[c for c in features if c not in cat]
    prep=ColumnTransformer([("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),num),("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]),cat)])
    model=Pipeline([("prep",prep),("model",LogisticRegression(max_iter=1000,class_weight="balanced"))])
    X=df[features]; y=df.adopted_simulated
    if y.nunique()>1:
        Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=7,stratify=y)
        model.fit(Xtr,ytr); pte=model.predict_proba(Xte)[:,1]
        auc=float(roc_auc_score(yte,pte)); ap=float(average_precision_score(yte,pte))
    else:
        model.fit(X,y); auc=ap=float("nan")
    model.fit(X,y); df=df.copy(); df["adoption_propensity"]=model.predict_proba(X)[:,1]
    km=KMeans(n_clusters=4,random_state=41,n_init=10)
    df["segment_cluster"]=km.fit_predict(df[["annual_revenue_usd_m","products_held","digital_activity_score","engagement_score"]])
    df["review_priority_score"]=(.50*df.adoption_propensity+.35*(df.estimated_wallet_gap_usd_m/df.estimated_wallet_gap_usd_m.max())+.15*df.engagement_score).clip(0,1)
    df["priority_band"]=pd.qcut(df.review_priority_score.rank(method="first"),4,labels=["Monitor","Explore","High review","Priority review"])
    df["recommended_review"]="Investigate product need and relationship context; validate eligibility, suitability, and evidence before action."
    return df,auc,ap

df=build_data()
scores,auc,ap=score(df)
with st.sidebar:
    st.header("Portfolio controls")
    regions=st.multiselect("Region",sorted(scores.region.unique()),default=sorted(scores.region.unique()))
    sectors=st.multiselect("Sector",sorted(scores.sector.unique()),default=sorted(scores.sector.unique()))
    priorities=st.multiselect("Review priority",list(scores.priority_band.cat.categories),default=list(scores.priority_band.cat.categories))
    min_prop=st.slider("Minimum adoption propensity",0.0,1.0,0.0,0.05)
    st.caption("All data are generated synthetically in this app.")
view=scores[scores.region.isin(regions)&scores.sector.isin(sectors)&scores.priority_band.isin(priorities)&(scores.adoption_propensity>=min_prop)].copy()
tabs=st.tabs(["Portfolio overview","Client explorer","RM action queue","Evidence & model review","AI analyst"])
with tabs[0]:
    a,b,c,d=st.columns(4)
    a.metric("Synthetic clients",f"{len(view):,}")
    b.metric("Mean propensity",f"{view.adoption_propensity.mean():.1%}" if len(view) else "—")
    c.metric("Median wallet-gap proxy",f"${view.estimated_wallet_gap_usd_m.median():,.1f}m" if len(view) else "—")
    d.metric("Priority review",f"{(view.priority_band=='Priority review').sum():,}")
    l,r=st.columns(2)
    with l: st.plotly_chart(px.bar(view.groupby("sector",as_index=False).size(),x="sector",y="size",title="Portfolio by sector"),use_container_width=True)
    with r: st.plotly_chart(px.scatter(view,x="adoption_propensity",y="estimated_wallet_gap_usd_m",color="priority_band",size="annual_revenue_usd_m",hover_name="client_id",title="Propensity vs wallet-gap proxy"),use_container_width=True)
    st.subheader("Interpretation guardrails")
    st.markdown("- Propensity is predictive, not causal.\n- Wallet gap is a simulated proxy, not observed bank wallet.\n- Priority is a review heuristic, not a credit, pricing, suitability, or client-treatment decision.")
    st.dataframe(view.sort_values("review_priority_score",ascending=False).head(15),use_container_width=True,hide_index=True)
with tabs[1]:
    q=st.text_input("Search synthetic client ID",placeholder="SYN-00042")
    filtered=view[view.client_id.str.contains(q,case=False)] if q else view
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.download_button("Export filtered client table",filtered.to_csv(index=False).encode(),file_name="client_scores.csv",mime="text/csv")
with tabs[2]:
    queue=view.sort_values("review_priority_score",ascending=False)[["client_id","sector","region","relationship_tenure_years","products_held","adoption_propensity","estimated_wallet_gap_usd_m","review_priority_score","priority_band","recommended_review"]]
    st.caption(f"{len(queue)} review prompts. Human review required; no automatic contact occurs.")
    st.dataframe(queue,use_container_width=True,hide_index=True)
    st.download_button("Export RM review queue",queue.to_csv(index=False).encode(),file_name="rm_review_queue.csv",mime="text/csv")
with tabs[3]:
    st.subheader("Model and evidence review")
    x,y=st.columns(2); x.metric("Holdout ROC-AUC",f"{auc:.3f}" if np.isfinite(auc) else "N/A"); y.metric("Holdout average precision",f"{ap:.3f}" if np.isfinite(ap) else "N/A")
    st.write({"rows":len(scores),"unique_client_ids":int(scores.client_id.nunique()),"propensity_in_range":bool(scores.adoption_propensity.between(0,1).all()),"negative_wallet_proxy":int((scores.estimated_wallet_gap_usd_m<0).sum()),"data_status":"synthetic"})
    st.markdown("**Limitations:** Synthetic outcomes, illustrative feature relationships, no external validation, no drift monitoring, no causal claim, and no production governance sign-off.")
    st.download_button("Download synthetic data",df.to_csv(index=False).encode(),file_name="synthetic_clients.csv",mime="text/csv")
with tabs[4]:
    st.subheader("AI-assisted aggregate analysis")
    st.caption("Optional Groq integration. Only aggregate synthetic metrics should be sent; never send real or confidential client data.")
    question=st.text_area("Business question","Which segments should coverage investigate first, and what evidence gaps remain?")
    agg={"client_count":int(len(view)),"mean_propensity":round(float(view.adoption_propensity.mean()),4) if len(view) else None,"median_wallet_gap_usd_m":round(float(view.estimated_wallet_gap_usd_m.median()),3) if len(view) else None,"priority_counts":view.priority_band.astype(str).value_counts().to_dict(),"sector_counts":view.sector.value_counts().to_dict(),"synthetic_only":True}
    st.json(agg)
    if st.button("Ask Groq to draft an analysis",type="primary"):
        key=st.secrets.get("GROQ_API_KEY",os.environ.get("GROQ_API_KEY",""))
        if not key: st.error("Groq key not configured. Add GROQ_API_KEY to Streamlit Secrets; offline dashboard works without it.")
        else:
            try:
                from groq import Groq
                client=Groq(api_key=key)
                resp=client.chat.completions.create(model=st.secrets.get("GROQ_MODEL","meta-llama/llama-4-scout-17b-16e-instruct"),messages=[{"role":"system","content":"You are an evidence-aware CIB analytics assistant. Only use supplied synthetic aggregates. Distinguish prediction from causality. State limitations and require human review. Never recommend automatic client contact or regulated decisions."},{"role":"user","content":f"Business question: {question}\nSynthetic aggregates: {agg}"}],temperature=.2,max_tokens=700)
                st.markdown(resp.choices[0].message.content)
                st.warning("LLM output is an unverified draft. Check every claim and require human review.")
            except Exception as e: st.error(f"Groq request failed: {e}")
st.divider()
st.caption("Portfolio project · synthetic data only · independently built for demonstrating client intelligence analytics.")
