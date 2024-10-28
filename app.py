import streamlit as st
import enigma as em

### --- INTRODUCTION --- ###

# name the app in browser
st.set_page_config("Enigma Machine")

# set title
st.title("Welcome to Enigma!")

# set image
st.image("enigma_machine.png", caption="Christian Lendl on Unsplash")

# introductory text and overview
st.write("The engima machine is among the best known of text ciphers. Developed and deployed by the Nazis during the Second World War, uncovering the workings of this electromechanical encoding device was a top priority for the Allies in the Atlantic theatre. Understanding enemy messages was the difference between life and death.")
st.write("Here you encrypt and decrypt messages in the same way that Axis powers made use of the Enigma Machine during the Second World War.")
st.divider()

# using the machine
st.subheader("Using the Machine")
st.write("To encrypt a message, simply write in the text input and hit enter. If you have received a message encrypted with Enigma, then you can enter the cipher text and hit enter to get the original message. But remember: to decrypt a message you must use the same settings that were used to encrypt the message.")
st.write("The original Enigma Machine didn't use a random seed, but one is used here to increase variation. The other settings are 1) choosing the plugboard and 2) setting the order of the rotors. This mimics how the real Enigma Machine would have been set up.")
st.divider()

# machine configuration
st.subheader("Settings")
st.write("Here you configure the Machine settings. If you have received an ecrypted message, then you should use the same settings that the Encrypter used.")
st.write("Although the original Enigma Machine was electromechanical and this 'Machine' is created with software, the encoding process is replicated exactly. Click to read more about this project and the Enigma Machine.")


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

st.subheader("Encrypt your message")

# input text
input_text = st.text_input("Enter your plaintext or ciphertext here to encrypt or decrypt:", help="Enter only letters and fullstop characters")

# output text
output_text = machine.encrypt(input_text)

# show output
st.text_area("Encrypted/decrypted text:", output_text)