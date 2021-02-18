# location of local authentication logs to insert to db (update these paths if needed)
auth_raw_files = [
    '../../dataset/auth_C1DOM1.txt',
    '../../dataset/auth_C2DOM1.txt',
    '../../dataset/auth_C3DOM1.txt',
    '../../dataset/auth_C4DOM1.txt',
    '../../dataset/auth_C5DOM1.txt',
    '../../dataset/auth_C6DOM1.txt',
    '../../dataset/auth_C7DOM1.txt',
    '../../dataset/auth_ANONYMOUS-LOGONC5828.txt',
    '../../dataset/auth_ANONYMOUS-LOGONC5919.txt'
]

authlogs = []

for auth_file in auth_raw_files:
    with open(auth_file) as f:
        all_lines = f.readlines()
        for line in all_lines:
            # cleaning data
            line = line.strip()
            tokens = line.split(',')
            for i in range(len(tokens)):
                if (tokens[i] == '?'):
                    tokens[i] = None
            
            authlogs.append(tokens)



