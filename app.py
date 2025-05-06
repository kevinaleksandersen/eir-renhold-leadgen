import streamlit as st
import openai
import pandas as pd

openai.api_key = st.secrets["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"]

st.title("📞 Leadsgenerator for Eir Renhold")

st.markdown("Få forslag til bransjer og ringeliste basert på område og målgruppe.")

region = st.text_input("Geografisk område", "Trondheim")
target = st.text_input("Bransje", "Kontorbygg")
amount = st.number_input("Antall leads", min_value=1, max_value=100, value=10)

if st.button("Generer ringeliste"):
    with st.spinner("Henter forslag..."):
        prompt = f""" 
Du er en B2B-selger i renholdsbransjen i Norge. Finn {amount} relevante bedrifter innen "{target}" i området "{region}". 
For hver bedrift, finn kontaktperson i denne rekkefølgen:
1. Daglig leder
2. Innkjøpsansvarlig
3. HR-leder

Svar i tabellformat med kolonnene:
| Bedriftsnavn | Bransje | Lokasjon | Kontaktperson | Stilling | Kommentar |
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        output = response['choices'][0]['message']['content']
        st.markdown(output)

        if "| Bedriftsnavn" in output:
            try:
                table_data = output.split("\n")
                rows = [r for r in table_data if "|" in r and "Bedriftsnavn" not in r]
                clean_rows = [r.split("|")[1:-1] for r in rows]
                df = pd.DataFrame(clean_rows, columns=["Bedriftsnavn", "Bransje", "Lokasjon", "Kontaktperson", "Stilling", "Kommentar"])
                st.subheader("📋 Ringeliste (strukturert)")
                st.dataframe(df)
                st.download_button("📥 Last ned som Excel", df.to_csv(index=False).encode(), file_name="ringeliste.csv")
            except:
                st.info("Klarte ikke å hente ut tabellen strukturert.")
