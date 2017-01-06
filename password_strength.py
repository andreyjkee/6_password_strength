import getpass
import re


def get_password_strength(password):
    strength = 1
    recomendations = []
    if any([__has_offensive_words(password), __has_personal_info(password)]):
        recomendations.append('Не используйте запрещенные слова, и личную информацию в пароле')
        return strength
    strength = 0
    if __is_case_sensitive(password):
        strength += 2
    else:
        recomendations.append('Используйте разный регистр букв')
    if __has_number(password):
        strength += 1
    else:
        recomendations.append('Пароль не содержит цифр')
    if __valid_password_length(password):
        strength += 2
    else:
        recomendations.append('Используйте длинные пароли, не менее 8 символов')
    if __has_special_chars(password):
        strength += 5
    else:
        recomendations.append('Используйте специальные символы в пароле')
    return strength, recomendations

def __is_case_sensitive(password):
    return password != password.lower()

def __has_number(password):
    return bool(re.findall(r'\d', password))

def __has_special_chars(password):
    patter_str = r'[`\~\!\@\#\$\%\^\&\*\(\)\_\-\+\{\}\[\]\\\|\:\;\"\'\<\>\,\.\?\/]'
    return bool(re.findall(patter_str, password))

def __has_offensive_words(password):
    black_list = ['test', 'Password1', '12345', 'password']
    pattern = re.compile('(' + '|'.join(black_list) + ')', re.IGNORECASE)
    return bool(pattern.findall(password))

def __has_personal_info(password):
    info_words = ['realname', 'cat name']
    pattern = re.compile('(' + '|'.join(info_words) + ')', re.IGNORECASE)
    return bool(pattern.findall(password))

def __valid_password_length(password, length=8):
    return len(password) >= length


if __name__ == '__main__':
    password = getpass.getpass('Enter password:')
    strength, recomendations = get_password_strength(password)
    print('Оценка сложности пароля (макс. 10): {0}'.format(strength))
    if recomendations:
        print('Рекомендации по повышению взломостойкости пароля:')
        for recom in recomendations:
            print('\t{0}'.format(recom))
