import sys
import string
import random


'''---------------------------------------------
this function parses the script input arguments
and returns the relevant input, if any.

    - if input string is valid,
      the input string will be returned.

    - if input string is no valid,
      False will be returned.

    - if '--random:<#>' is detected,
      a random string will be returned.

    - if '#' on '--random:<#>' is not valid,
      an empty string will be returned.
---------------------------------------------'''
def argument_parser():

    try:
        # checking if an argument was passed through
        user_input = sys.argv[1]

        # checking if the input argument is '--random:<num>'
        if user_input[0:9] == '--random:':
            user_input = user_input[9:]

            # checking if the input is a valid numeric value
            try:
                int(user_input)
                bold_start = "\033[1m"
                bold_end = "\033[0;0m"
                print ('\n\t✅  Generating a random string of maximum ' + str(bold_start) + str(user_input) + str(bold_end) + ' characters.')

                # returning a randomally generated string
                return get_random_string(int(user_input))

            except:
                print ('\n\t⛔️  To generate a random string, please enter a valid numeric value.')
                print ('\t   Example: --random:8 or --random:146\n')

                # returning an empty string
                return ''


        # checking if the input is a valid alphabetic value
        elif str.isalpha(user_input):

            bold_start = "\033[1m"
            bold_end = "\033[0;0m"
            print ('\n\t✅  Detected a string as an input: ' + str(bold_start) + str(user_input) + str(bold_end))

            # returning user's input string
            return user_input

        # the input string is not valid :\
        else:
            print ('\n\t⛔️  Input string must include only hexadecimal characters:')
            print ('\t  ', string.ascii_lowercase)
            print ('\t  ', string.ascii_uppercase, '\n')
            return False

    # no input was detected
    except:
        print ('\n\tℹ️  No input string was detected.')

        # returning an empty string
        return ''



'''---------------------------------------------
this function generates a random alphabetic
string.
max_length: the maximum length of the random string
if no max_length is given, max_length is 10.
---------------------------------------------'''
def get_random_string(max_length=10):

    random_string = ""

    # generating sequences to create a sting worth encoding
    sequences = []
    random_string_length = 0
    while random_string_length < max_length:
        num = random.randint(1,9)
        if (random_string_length + num) > max_length:
            break
        else:
            sequences.append(num)
            random_string_length = sum(sequences)

    # generating the string using random alphabetic characters
    for num in sequences:
        random_string = random_string + random.choice(string.ascii_letters) * num


    # printing the randomly generated string
    bold_start = "\033[1m"
    bold_end = "\033[0;0m"
    print ('\n\t✅  Generated the following random string: ' + bold_start + random_string + bold_end + ' (length == ' + str(len(random_string)) + ')')

    # returning the random string
    return random_string



'''---------------------------------------------
this function receives a string and returns
an encoded version of this string, that could
be decoded using 'string_decoder(input_string)'.
---------------------------------------------'''
def string_encoder(input_string):

    # making sure that input_string is alphabetic
    try:
        str.isalpha(input_string)

        encoded_string = ''
        current_char = input_string[0]
        current_char_count = 0

        for char in input_string:

            # counting consecutive characters
            if char == current_char:
                current_char_count+=1

            else:
                encoded_string = encoded_string + str(current_char_count) + current_char
                current_char = char
                current_char_count = 1

                # checking if the encoded string is longer than original one
                if len(encoded_string) >= len(input_string):
                    print ('\n\tℹ️  Cannot effiently encode the input string. Returning original string.')
                    encoded_string = input_string
                    return encoded_string

        # adding the last pair of encoded characters
        encoded_string = encoded_string + str(current_char_count) + current_char


        return encoded_string

    except:
        print ('\n\t⛔️  Input string must include only hexadecimal characters:')
        print ('\t  ', string.ascii_lowercase)
        print ('\t  ', string.ascii_uppercase)
        return




'''---------------------------------------------
this function receives an encoded string,
that was encoded using 'string_encoder(input_string)',
and returns it in it original form.
---------------------------------------------'''
def string_decoder(input_string):

    # checking if NOT input_string is an encoded string
    # for input_string to be an encoded string, it should satisfy:
        # - numbers of characters is even
        # - number of digits in string == half the string length
    if len(input_string) % 2 != 0:
        print ('\n\t⛔️  Input is not an encoded string.')
        return input_string

    digit_count = 0
    for char in input_string:
        if char.isdigit():
            digit_count+=1

    if len(input_string)/2 != digit_count:
        print ('\n\t⛔️  Input is not an encoded string.')
        return input_string

    # checking that the input string is alphabetic
    try:
        str.isalpha(input_string)

        decoded_string = ''
        current_char = ''
        current_char_multiplier = 0

        for char in input_string:

            # if char is a number, this is a multiplier
            try:
                int(char)
                current_char_multiplier = int(char)

            # multiplying the character that is right after the detected number
            except:
                current_char = char
                decoded_string = decoded_string + (current_char * current_char_multiplier)
                continue

        # returning the decoded string
        return decoded_string

    except:
        print ('\n\t⛔️  Input string must include only hexadecimal characters:')
        print ('\t  ', string.ascii_lowercase)
        print ('\t  ', string.ascii_uppercase)
        return



def main():

    # getting user input
    string_to_encode = argument_parser()

    # generating random string, in needed
    if string_to_encode == '':
        string_to_encode = get_random_string()

    # exitting if the input is invalid
    elif string_to_encode == False:
        return

    # encoding the string
    encoded = string_encoder(string_to_encode)
    bold_start = "\033[1m"
    bold_end = "\033[0;0m"
    print ('\n\t🏁  Encoded string: ' + bold_start + encoded + bold_end)

    # decoding the string, for fun :)
    decoded = string_decoder(encoded)

    # printing the decoded string
    bold_start = "\033[1m"
    bold_end = "\033[0;0m"
    match = decoded == string_to_encode
    print ('\n\t🔍  Decoded string: ' + bold_start + decoded + bold_end + ' (match == ' + str(match) + ')\n')



if __name__ == "__main__":
    main()
