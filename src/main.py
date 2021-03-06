from TeamScrap import TeamScrap
from colorama import Fore, Style
from datetime import datetime, timedelta
from crypt import Crypt
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

def clear_token():
	encrypted_token_file = open('token.txt', 'wb')
	encrypted_token_file.write(''.encode())
	encrypted_token_file.close()

def parse_teams_date_time(date_time):
	all_date_parsed = date_time.split('T')
	date_parsed = all_date_parsed[0].split('-')
	hour_parsed = all_date_parsed[1].replace('Z', '').split(':')

	return [date_parsed, hour_parsed]

def parse_date_time(date_time):
	all_date_parsed = str(date_time).split(' ')
	date_parsed = all_date_parsed[0].split('-')
	hour_parsed = all_date_parsed[1].split(':')

	return [date_parsed, hour_parsed]

print(ascii_art.return_ascii())

print('Tentando encontrar o Bearer token...\n')

c = Crypt()

encrypted_token_file = open('token.txt', 'rb')
encrypted_token = encrypted_token_file.read()
encrypted_token_file.close()

if not encrypted_token:
	print(f'{Fore.YELLOW}Não conseguimos localizar seu token salvo em cache, digite manualmente{Style.RESET_ALL}')
	print('Digite o seu bearer token do Teams: (? para ajuda)')
	bearer_token = str(input('')).strip()

	if bearer_token == '?':
		tutorial()

	print('\n')
	print(Fore.YELLOW + '!' + Style.RESET_ALL)
	print(Fore.YELLOW + 'Não se preocupe, não enviaremos essa informação para nenhum local, apenas será encriptada na sua máquina como cache.' + Style.RESET_ALL)
	print(Fore.YELLOW + '!' + Style.RESET_ALL)
	print('\n')

	key_file = open('key.key', 'rb')
	key = key_file.read()
	key_file.close()

	if not key:
		c.generate_new_key()
		c.encrypt(bearer_token)
	else:
		c.encrypt(bearer_token)

	encrypted_token_file = open('token.txt', 'rb')
	encrypted_token = encrypted_token_file.read()
	encrypted_token_file.close()

	if not encrypted_token:
		print(f'{Fore.RED}Ocorreu um erro, tente novamente{Style.RESET_ALL}')

	original_token = c.decrypt(encrypted_token)
else:
	try:
		original_token = c.decrypt(encrypted_token)
	except Exception as err:
		print(f'{Fore.RED}{err}{Style.RESET_ALL}')
		clear_token()
		exit()

	print(f'{Fore.BLUE}Seu token foi encontrado em cache!{Style.RESET_ALL}\n')

print('Pegando assignments... (Isso pode demorar alguns minutos)\n')

ts = TeamScrap(original_token)

try:
	classes_assignments = ts.get_all_classes_assignments()
except Exception as err:
	print(f'{Fore.RED}{err}{Style.RESET_ALL}\n')
	print(f'{Fore.RED}Verifique se o token não expirou ou está correto{Style.RESET_ALL}\n')
	clear_token()
	exit()
	
overdue_assignments = 0

print('=' * 100)
for class_assignment in classes_assignments:
	due_date_time = class_assignment['assignmentInfo']['dueDateTime']
	[date_parsed, hours_parsed] = parse_teams_date_time(due_date_time)

	date_init = datetime.now()
	date_final = datetime(year=int(date_parsed[0]), month=int(date_parsed[1]), day=int(date_parsed[2]), hour=int(hours_parsed[0]), minute=int(hours_parsed[1]), second=int(hours_parsed[2]))

	date_final -= timedelta(hours=3)

	[final_date_parsed, final_hours_parsed] = parse_date_time(date_final)

	remaining_date = date_final - date_init

	remaining_date_parsed = str(remaining_date).split(',')

	if len(remaining_date_parsed) > 1:
		remaining_days = int(remaining_date_parsed[0].strip().split(' ')[0])
		remaining_hours = remaining_date_parsed[1].strip().split(':')
	else:
		remaining_hours = remaining_date_parsed[0].strip().split(':')

	print('\n')
	print(f'{Fore.GREEN}Matéria:{Style.RESET_ALL} {class_assignment["classInfo"][0]["name"]}')
	print(f"{Fore.GREEN}Descrição:{Style.RESET_ALL} {class_assignment['assignmentInfo']['displayName']}")
	print(f'{Fore.GREEN}Data de entrega:{Style.RESET_ALL} {final_date_parsed[2]}/{final_date_parsed[1]}/{final_date_parsed[0]} às {final_hours_parsed[0]}:{final_hours_parsed[1]}:{final_hours_parsed[2]}')
	
	if len(remaining_date_parsed) == 1:
		print(f'{Fore.GREEN}Tempo restante:{Style.RESET_ALL} {remaining_hours[0]} horas {remaining_hours[1]} minutos e {int(float(remaining_hours[2]))} segundos')
	elif int(remaining_days) < 0:
		print(f'{Fore.RED}Assignment em atraso!{Style.RESET_ALL}')
		overdue_assignments += 1
	else:
		print(f'{Fore.GREEN}Tempo restante:{Style.RESET_ALL} {remaining_days} dias, {remaining_hours[0]} horas, {remaining_hours[1]} minutos e {int(float(remaining_hours[2]))} segundos')
	print('\n')
	print('=' * 100)

print('\n')
print(f'{Fore.GREEN}Total de assignments:{Style.RESET_ALL} {len(classes_assignments)}')
print(f'{Fore.RED}Total de assignments em atraso:{Style.RESET_ALL} {overdue_assignments}')