from TeamScrap import TeamScrap
from colorama import Fore, Style
import ascii_art

def tutorial():
	print(f'\nFaça login com a sua conta institucional no site{Fore.RED} https://teams.microsoft.com{Style.RESET_ALL}')
	print(f'Após fazer o login, aperte F12 e vá em{Fore.RED} Network{Style.RESET_ALL}')
	print(f'Vá para o menu de tarefas do teams e espere aparecer{Fore.RED} classes{Style.RESET_ALL} no devtools')
	print(f'Clique em classes, vá para a aba Headers e desça até achar a{Fore.RED} Request Headers{Style.RESET_ALL}')
	print(f'Encontre a palavra{Fore.RED} Authorization{Style.RESET_ALL} e copie todas as letras aleatórias depois da palavra{Fore.RED} Bearer {Style.RESET_ALL} {Fore.YELLOW}(Lembre-se que é apenas para copiar as letras que pertencem ao header Authorization){Style.RESET_ALL}')
	print(f'Após fazer isso, volte para o programa e cole esse token aqui\n')	
	print(Fore.YELLOW + 'Esse token pode parar de funcionar depois de um tempo e será necessário fazer esse processo novamente!' + Style.RESET_ALL)
	print('\n')
	exit(0)

print(ascii_art.return_ascii())

print('Tentando encontrar o Bearer token...\n')
print('Digite o seu bearer token do Teams: (? para ajuda)')
bearer_token = str(input(''))

if bearer_token == '?':
	tutorial()

print('\n')
print(Fore.YELLOW + '!' + Style.RESET_ALL)
print(Fore.YELLOW + 'Não se preocupe, não guardaremos essa informação.' + Style.RESET_ALL)
print(Fore.YELLOW + '!' + Style.RESET_ALL)
print('\n')

print('Pegando tarefas... (Isso pode demorar alguns minutos)\n')

ts = TeamScrap(bearer_token.strip())
classes_assignments = ts.get_all_classes_assingments()

for class_assignment in classes_assignments:
	print('=' * 100)
	print('\n')
	print(f'Matéria: {class_assignment["classInfo"][0]["name"]}')
	print(class_assignment['assignmentInfo']['displayName'])
	print(f'Data de entrega: {class_assignment["assignmentInfo"]["dueDateTime"]}')
	print('\n')
	print('=' * 100)
