def get_chinese(path):
    with open(path, 'r') as f:
        chinese = f.read()
        f.close()
        return chinese

