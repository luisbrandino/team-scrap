from cryptography.fernet import Fernet

class Crypt:
	def __init__(self):
		pass

	def generate_new_key(self):
		key = Fernet.generate_key()
		key_file = open('key.key', 'wb')
		key_file.write(key)
		key_file.close()

	def encrypt(self, token):
		if not token: return print('Nenhum token foi providênciado'); exit()

		key_file = open('key.key', 'rb')
		key = key_file.read()
		key_file.close()

		if not key: return print('Nenhuma key foi providênciada'); exit()

		f = Fernet(key)
		encrypt_token = f.encrypt(token.encode())

		token_file = open('token.txt', 'wb')
		token_file.write(encrypt_token)
		token_file.close()

	def decrypt(self, encrypted):
		if not encrypted: return exit()

		key_file = open('key.key', 'rb')
		key = key_file.read()
		key_file.close()

		if not key:
			key = self.generate_new_key()

		f = Fernet(key)

		try:
			decrypted = f.decrypt(encrypted)
			original_token = decrypted.decode()

			return original_token
		except:
			raise Exception('Não foi possível decryptar o arquivo')
			
			return 