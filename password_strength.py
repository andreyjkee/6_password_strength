import argparse
import getpass
import re

global black_list

class PasswordErrorsEnum():
    offensive_words = 'Не используйте запрещенные слова, и личную информацию в пароле'
    mixed_case = 'Используйте разный регистр букв'
    digits = 'Пароль не содержит цифр'
    length = 'Используйте длинные пароли, не менее 8 символов'
    special_chars = 'Используйте специальные символы в пароле'


def get_password_strength(password):
    strength = 1
    recomendations = []
    if __has_offensive_words(password):
        recomendations.append(PasswordErrorsEnum.offensive_words)
        return strength, recomendations
    strength = 0
    if __is_case_sensitive(password):
        strength += 2
    else:
        recomendations.append(PasswordErrorsEnum.mixed_case)
    if __has_number(password):
        strength += 1
    else:
        recomendations.append(PasswordErrorsEnum.digits)
    if __is_valid_password_length(password):
        strength += 2
    else:
        recomendations.append(PasswordErrorsEnum.length)
    if __has_special_chars(password):
        strength += 5
    else:
        recomendations.append(PasswordErrorsEnum.special_chars)
    return strength, recomendations

def __is_case_sensitive(password):
    return password != password.lower()

def __has_number(password):
    return bool(re.findall(r'\d', password))

def __has_special_chars(password):
    patter_str = r'[`~!@#$%^&*()_{}[]|\+-:;"<>,.?]'
    return bool(re.findall(patter_str, password))

def __read_list_from_file(filestream):
    with filestream as f:
        return [line.rstrip('\n') for line in f.readlines()]

def __has_offensive_words(password):
    if not black_list:
        return False
    pattern = re.compile('(' + '|'.join(black_list) + ')', re.IGNORECASE)
    return bool(pattern.findall(password))

def __is_valid_password_length(password, length=8):
    return len(password) >= length


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check password strength")
    parser.add_argument("-b", "--black-list", type=argparse.FileType('r'), dest="blacklist")
    parser.add_argument("-l", "--length", type=int, default=8, help='minimum password length')
    options = parser.parse_args()
    if options.blacklist:
        black_list = __read_list_from_file(options.blacklist)
    password = getpass.getpass('Enter password:')
    strength, recomendations = get_password_strength(password)
    print('Оценка сложности пароля (макс. 10): {0}'.format(strength))
    if recomendations:
        print('Рекомендации по повышению взломостойкости пароля:')
        for recom in recomendations:
            print('\t{0}'.format(recom))
