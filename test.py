from subprocess import Popen, PIPE

sim = f'python3 main.py sim'
com = f'python3 main.py com'


def test_word_sim():
    path = f'test/word.f'
    cmd = f'{sim} {path}'
    p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out = str(out.decode("utf-8"))
    expected = f'3\n'
    print(f'Test: Simulate Word     ' + ('✔️' if out == expected else '❌'))


def test_word_com():
    path = f'test/word.f'
    cmd = f'{com} {path}'
    p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out = str(out.decode("utf-8"))
    expected = f'3'
    print(f'Test: Compile Word      ' + ('✔️' if out == expected else '❌'))


def main():
    test_word_sim()
    test_word_com()


if __name__ == "__main__":
    main()
