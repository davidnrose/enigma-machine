import streamlit as st
import enigma as em

### --- INTRODUCTION --- ###

# name the app in browser
st.set_page_config("Enigma Machine")

# set title
st.title("Welcome to Enigma!")

# set image
st.image("enigma_machine.jpg", caption="Christian Lendl on Unsplash")

# introductory text and overview
st.write("Some information about the enigma machine and how to use it")
st.write("Here you encrypt and decrypt messages in the same way that Axis powers made use of the Enigma Machine during the Second World War.")

st.divider()

# machine configuration
st.subheader("Configure the Machine")
st.write("Here you configure the Machine settings. If you have received an ecrypted message, then you should use the same settings that the Encrypter used.")

# initialise columns
col1, col2 = st.columns(2, gap="medium")

# define plugboard and rotor options
rotors = ["Rotor I", "Rotor IV", "Rotor V"]

plugboards = {"plug1": "AR-XN-KG", "plug2": "CG-TE-HJ", "plug3": "AV-BC-IZ"}
plugboard_options = [plugboards["plug1"], plugboards["plug2"], plugboards["plug3"]]

with col1:
    seed = st.number_input("Set the Random Seed", min_value=1, max_value=9999, value=1234)

    st.write("Plugboard")
    plugboard_selected = st.radio("Select plugboard", options=plugboard_options)


with col2:
    rotor1 = st.selectbox("Position 1", options=rotors, index=0, placeholder="Select a Rotor")
    rotor2 = st.selectbox("Position 2", options=rotors, index=2, placeholder="Select a Rotor")
    rotor3 = st.selectbox("Position 3", options=rotors, index=1, placeholder="Select a Rotor")

st.divider()

### --- INITIALISE AND COMPILE --- ###

# initialise alphabet object
alpha = em.Alphabet()

# initialise rotors
I = em.Rotor(seed, alpha)
IV = em.Rotor(seed+1, alpha)
V = em.Rotor(seed+2, alpha)

# order rotors
def return_rotor(rotor):
    if rotor == "Rotor I":
        return I
    elif rotor == "Rotor IV":
        return IV
    elif rotor == "Rotor V":
        return V

chosen_rotors = [rotor1, rotor2, rotor3]
rotors_ord = [return_rotor(r) for r in chosen_rotors]

# initialise plugboard
plug_pairs = [p.lower() for p in plugboard_selected.split("-")]
p = em.Plugboard(alpha, plug_pairs)

# initiate reflector
R = em.Reflector(seed+4, alpha)

# compile machine
machine = em.Machine(p, rotors_ord, R)

### --- ENCRYPT AND DECRYPT --- ###

# input text
input_text = st.text_input("Enter your plaintext or ciphertext here to encrypt or decrypt:", help="Enter only letters and fullstop characters")

# output text
output_text = machine.encrypt(input_text)

# show output
st.text_area("Encrypted/decrypted text:", output_text)