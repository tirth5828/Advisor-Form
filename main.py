import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json



# Load Firebase credentials from Streamlit secrets
firebase_secrets = st.secrets["firebase"]

cred = credentials.Certificate({
    "type": firebase_secrets["type"],
    "project_id": firebase_secrets["project_id"],
    "private_key_id": firebase_secrets["private_key_id"],
    "private_key": firebase_secrets["private_key"].replace("\\n", "\n"),
    "client_email": firebase_secrets["client_email"],
    "client_id": firebase_secrets["client_id"],
    "auth_uri": firebase_secrets["auth_uri"],
    "token_uri": firebase_secrets["token_uri"],
    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
})


# Initialize Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def main():
    st.title("Advisor Planning - Income Ki Ultimate RAAFTAR (Aug-Sep 2024)")

    # Advisor Code
    advisor_code = st.text_input("Advisor Code", key="advisor_code")
    if not advisor_code:
        st.warning("Please enter the Advisor Code.")

    # Advisor Name
    advisor_name = st.text_input("Advisor Name", key="advisor_name")
    if not advisor_name:
        st.warning("Please enter the Advisor Name.")

    # For NLA / Advisor only (01st Aug 2024 to 16th Sep 2024)
    st.subheader("For NLA / Advisor only (01st Aug 2024 to 16th Sep 2024)")
    rewards_nla = {
        "Select EP Goal": 0,
        "I am not a NLA": 0, 
        "70000 EP 7500 Reward": 70000,
        "125000 EP 15000 Reward": 125000
    }
    nlp_ep_goal = st.selectbox("Select EP Goal", list(rewards_nla.keys()), key="nlp_ep_goal")
    if nlp_ep_goal == "Select EP Goal":
        st.warning("Please select an EP Goal for NLA/Advisor.")

    # Planning for Slab Achievement Aug - Sep 2024
    st.subheader("Planning for Slab Achievement Aug - Sep 2024")
    rewards_slab = {
        "Select EP Goal": 0,
        "200000 EP 7500 Reward": 200000,
        "350000 EP 12500 Reward": 350000,
        "500000 EP 20000 Reward": 500000,
        "700000 EP 30000 Reward": 700000,
        "900000 EP 45000 Reward": 900000,
        "1300000 EP 75000 Reward": 1300000,
        "1900000 EP 125000 Reward": 1900000,
        "2500000 EP 200000 Reward": 2500000,
        "3200000 EP 300000 Reward": 3200000,
        "4000000 EP 400000 Reward": 4000000,
        "5000000 EP 550000 Reward": 5000000,
        "7500000 EP 900000 Reward": 7500000,
        "9000000 EP 1250000 Reward": 9000000,
        "12500000 EP 2000000 Reward": 12500000,
    }
    slab_achievement_ep_goal = st.selectbox("Select EP Goal", list(rewards_slab.keys()), key="slab_achievement_ep_goal")
    if slab_achievement_ep_goal == "Select EP Goal":
        st.warning("Please select an EP Goal for Slab Achievement.")
        
    # WNBP Achieve Milestone Amount Aug - Sep 2024
    WNBP_Achieve_Milestone_Amount = st.number_input("WNBP Achieve Milestone Amount Aug - Sep 2024", key="WNBP_Achieve_Milestone_Amount")
    if not WNBP_Achieve_Milestone_Amount:
        st.warning("Please enter the WNBP Achieve Milestone Amount Aug - Sep 2024.")

    # WNBP Achieve Milestone
    st.subheader("WNBP Achieve Milestone")
    milestones = {
        "10th Aug": 11,
        "17th Aug": 18,
        "24th Aug": 27,
        "31st Aug": 36,
        "07th Sep": 52,
        "14th Sep": 66,
        "21st Sep": 82,
        "28th Sep": 100
    }
    for date, percentage in milestones.items():
        st.text(f"WNBP Achieve Milestone by {date} ({percentage}% of Target) - Rs. {percentage*WNBP_Achieve_Milestone_Amount/100}")

    # Achieve by September END
    st.subheader("What will I Achieve by September END")
    achievements = ["Quarter MDRT", "Half MDRT", "MDRT", "1.5 MDRT", "Double MDRT", "COT", "TOT"]
    selected_achievement = st.selectbox("Select Achievement", achievements, key="selected_achievement")
    if selected_achievement == "Select Achievement":
        st.warning("Please select an Achievement.")

    # Qualify for COT/TOT Strategy meet
    st.subheader("Will I Qualify for COT/TOT Strategy meet")
    qualify_cot_tot = st.radio(
        "Select Qualification",
        ["HALF MDRT by SEP 24 (min IOLac WNBP in JAS'24)", "1.5 MDRT by AUG 24"],
        key="qualify_cot_tot"
    )

    # Submit Button
    if st.button("Submit"):
        if advisor_code and advisor_name and nlp_ep_goal != "Select EP Goal" and slab_achievement_ep_goal != "Select EP Goal" and selected_achievement and WNBP_Achieve_Milestone_Amount!=0 and qualify_cot_tot:
            data = {
                "advisor_code": advisor_code,
                "advisor_name": advisor_name,
                "nlp_ep_goal": nlp_ep_goal,
                "slab_achievement_ep_goal": slab_achievement_ep_goal,
                "selected_achievement": selected_achievement,
                "WNBP_achieve_milestone_amount": WNBP_Achieve_Milestone_Amount,
                "qualify_cot_tot": qualify_cot_tot
            }
            db.collection("advisor_planning").add(data)
            st.success("Form submitted successfully!")
        else:
            st.error("Please fill all the required fields.")

if __name__ == "__main__":
    main()
