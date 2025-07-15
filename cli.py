import click
from cipher import UltimateCipher

@click.group()
def cli():
    """Ultimate Cipher CLI - A combination of Affine, Vigenere, Transposition, and XOR ciphers"""
    pass

@cli.command()
@click.option('--text', prompt='Enter text to encrypt', help='Text to encrypt')
@click.option('--affine-a', prompt='Enter Affine Key "a"', type=int, help='Affine cipher key a')
@click.option('--affine-b', prompt='Enter Affine Key "b"', type=int, help='Affine cipher key b')
@click.option('--vigenere-key', prompt='Enter Vigenere Key', help='Vigenere cipher key')
@click.option('--xor-key', prompt='Enter XOR Key', help='XOR cipher key')
def encrypt(text, affine_a, affine_b, vigenere_key, xor_key):
    """Encrypt text using the Ultimate Cipher"""
    cipher = UltimateCipher()
    try:
        result = cipher.encrypt(text, affine_a, affine_b, vigenere_key, xor_key)
        click.echo(f"Encrypted text: {result}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--text', prompt='Enter text to decrypt', help='Text to decrypt')
@click.option('--affine-a', prompt='Enter Affine Key "a"', type=int, help='Affine cipher key a')
@click.option('--affine-b', prompt='Enter Affine Key "b"', type=int, help='Affine cipher key b')
@click.option('--vigenere-key', prompt='Enter Vigenere Key', help='Vigenere cipher key')
@click.option('--xor-key', prompt='Enter XOR Key', help='XOR cipher key')
def decrypt(text, affine_a, affine_b, vigenere_key, xor_key):
    """Decrypt text using the Ultimate Cipher"""
    cipher = UltimateCipher()
    try:
        result = cipher.decrypt(text, affine_a, affine_b, vigenere_key, xor_key)
        click.echo(f"Decrypted text: {result}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli() 