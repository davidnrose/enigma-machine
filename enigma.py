import numpy as np
import pandas as pd

# create alphabet class for quickly creating rotors, plugboard, and reflector, and initialise the alphabet
class Alphabet():
    def __init__(self):
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
                        "j", "k", "l", "m", "n", "o", "p", "q", "r",
                        "s", "t", "u", "v", "w", "x", "y", "z"]

    def scramble(self, seed):
        np.random.seed(seed)
        return [str(a) for a in list(np.random.choice(self.letters[:], size=26, replace=False))]


    def plugboard(self, pairs):
        board = self.letters[:]
        for p in pairs:
            p1 = board.index(p[0])
            p2 = board.index(p[1])
            board[p1], board[p2] = board[p2], board[p1]

        return board


# create plugboard object for swapping out letters
class Plugboard():
    def __init__(self, alpha, plug_pairs):
        self.left = alpha.letters[:]
        self.right = alpha.plugboard(plug_pairs)

    def setting(self):
        setting = pd.DataFrame(self.right, self.left)
        setting = setting.reset_index()
        setting.columns = ["left", "right"]
        return setting

    def forward(self, letter):
        return self.right.index(letter)

    def backward(self, idx):
        letter = self.right[idx]
        out_letter_idx = self.left.index(letter)
        return self.left[out_letter_idx]


class Rotor():
    def __init__(self, seed, alpha):
        self.left = alpha.letters[:]
        self.right = alpha.scramble(seed)
        self.rotation = 0
        self.left_config = alpha.letters[:]
        self.right = alpha.scramble(seed)

    def setting(self):
        setting = pd.DataFrame(self.right, self.left)
        setting = setting.reset_index()
        setting.columns = ["left", "right"]
        return setting

    def encrypt(self, in_idx, mode="fwd"):
        if mode == "fwd":
            letter = self.left[in_idx]
            out_idx = self.right.index(letter)

        elif mode == "bck":
            letter = self.right[in_idx]
            out_idx = self.left.index(letter)

        return out_idx

    def rotate(self):
        l_new_setting = self.left[1:]
        l_new_setting.append(self.left[0])
        self.left = l_new_setting

        r_new_setting = self.right[1:]
        r_new_setting.append(self.right[0])
        self.right = r_new_setting

        self.rotation += 1

    def reset_config(self):
        self.left = alpha.letters[:]
        self.right = alpha.scramble(seed)
        self.rotation = 0


class Reflector():
    def __init__(self, seed, alpha):
        letters = alpha.letters[:]

        left = list()
        right = list()
        np.random.seed(seed)

        for i in range(13):
            samp = np.random.choice(letters, size=2, replace=False)
            left_l = str(samp[0])
            right_l = str(samp[1])

            left.append(left_l)
            right.append(right_l)
            letters.remove(left_l)
            letters.remove(right_l)

        left = list(left + right)
        right = list(right + left)

        self.left = left
        self.right = right

    def setting(self):
        setting = pd.DataFrame(list(zip(self.left, self.right)), columns=["left", "right"])
        return setting

    def encrypt(self, in_idx):
        letter = self.left[in_idx]
        out_idx = self.right.index(letter)

        return out_idx


class Machine():
    def __init__(self, p, rotors, R):
        self.p = p
        self.r1 = rotors[0]
        self.r2 = rotors[1]
        self.r3 = rotors[2]
        self.R = R

        # keep original values for resetting the machine
        self.reset1 = rotors[0]
        self.reset2 = rotors[1]
        self.reset3 = rotors[2]

    def encrypt(self, text):
        out_text = list()

        # iterate through each character and encrypt
        for l in text:

            # check if punctuation
            if l == " ":
                out_text.append(" ")
            elif l == ".":
                out_text.append(".")
            elif l == ",":
                out_text.append(",")


            # else encrypt letters
            else:
                # check case and convert to lower
                if l.islower():
                    isLower = True
                else:
                    isLower = False
                l = l.lower()

                # pass through plugboard
                i = self.p.forward(l)

                # pass through rotors
                i = self.r1.encrypt(i)
                i = self.r2.encrypt(i)
                i = self.r3.encrypt(i)

                # reflect
                i = self.R.encrypt(i)

                # pass back trough rotors
                i = self.r3.encrypt(i, mode="bck")
                i = self.r2.encrypt(i, mode="bck")
                i = self.r1.encrypt(i, mode="bck")

                # pass through plugboard in reverse to convert back to letter
                i = self.p.backward(i)

                # rotate rotor 1 position
                if self.r1.rotation < 25:
                    self.r1.rotate()
                elif self.r1.rotation > 24 and self.r2.rotation < 25:
                    self.r2.rotate()
                elif self.r2.rotation > 24 and self.r3.rotation < 25:
                    self.r3.rotate()
                # unless all rotors have completed a rotation, then reset the counter
                else:
                    self.r1.rotation = 0
                    self.r2.rotation = 0
                    self.r3.rotation = 0

                if isLower == False:
                    i = i.upper()
                else:
                    pass

                # add characters to output
                out_text.append(i)

        # compile output
        out_text = "".join(out_text)
        print(out_text)

        return out_text

    def reset(self):
        self.r1.reset_config()
        self.r2.reset_config()
        self.r3.reset_config()

        self.r1.rotation = 0
        self.r2.rotation = 0
        self.r3.rotation = 0
