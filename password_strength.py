import argparse
import getpass
import re
from enum import Enum


class PasswordErrorsEnum(Enum):
    mixed_case = 1
    digits = 2
    special_chars = 3
    length = 4


password_errors_map = {
    PasswordErrorsEnum.mixed_case: 'Используйте разный регистр букв',
    PasswordErrorsEnum.digits: 'Пароль не содержит цифр',
    PasswordErrorsEnum.special_chars: 'Используйте специальные символы в пароле',
    PasswordErrorsEnum.length: 'Пароль сшишком короткий, это упрощает его перебор'
}

def get_password_strength(password):
    strength = 1
    recomendations = []
    if __has_number(password):
        strength += 1
    else:
        recomendations.append(PasswordErrorsEnum.digits)
    if len(password) >= 8:
        strength += 2
    else:
        recomendations.append(PasswordErrorsEnum.length)
    if __is_case_sensitive(password):
        strength += 2
    else:
        recomendations.append(PasswordErrorsEnum.mixed_case)
    if __has_special_chars(password):
        strength += 4
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check password strength")
    options = parser.parse_args()
    password = getpass.getpass('Enter password:')
    strength, recomendations = get_password_strength(password)
    print('Оценка сложности пароля (макс. 10): {0}'.format(strength))
    if recomendations:
        print('Рекомендации по повышению взломостойкости пароля:')
        for recom in recomendations:
            print('\t{0}'.format(password_errors_map.get(recom)))
