# String encoder
Command line script that receives a string and returns an encoded version of this string.
If no string is given, a random string is being generated.

![string encoder](demo.gif)

### How to use?
#### Run with input string:
```bash
$ python3 string_encoder.py <input_string>
```
Example:
```bash
$ python3 string_encoder.py AAABBBCCC
```

#### Test with random string and set a maximum length:
```bash
$ python3 string_encoder.py --random:<max_length>
```
Example:
```bash
$ python3 string_encoder.py --random:24
```

#### Test with random string of length 10:
```bash
$ python3 string_encoder.py
```
