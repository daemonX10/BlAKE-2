from flask import Flask, render_template, request, flash
import hashlib
import hmac
import binascii
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

def validate_blake2_key(form, field):
    if field.data:
        key_bytes = field.data.encode('utf-8')
        if len(key_bytes) > 64:
            raise ValidationError('BLAKE2 key must be 64 bytes or less')

def validate_blake2_salt(form, field):
    if field.data:
        salt_bytes = field.data.encode('utf-8')
        if len(salt_bytes) > 16:
            raise ValidationError('BLAKE2 salt must be 16 bytes or less')

class Blake2Form(FlaskForm):
    text = TextAreaField('Text to Hash', validators=[
        DataRequired(message='Please enter text to hash')
    ], render_kw={"rows": 4, "placeholder": "Enter your text here..."})
    
    action = SelectField(
        'Operation Type',
        choices=[
            ('generate', 'Generate Hash'),
            ('verify', 'Verify Data Integrity')
        ],
        validators=[DataRequired()]
    )
    
    hash_type = SelectField(
        'Hash Algorithm',
        choices=[
            ('blake2b', 'BLAKE2b (64-byte)'),
            ('blake2s', 'BLAKE2s (32-byte)'),
            ('blake2b_keyed', 'BLAKE2b with Key'),
            ('blake2s_keyed', 'BLAKE2s with Key')
        ],
        validators=[DataRequired()]
    )
    
    blake2_digest_size = SelectField(
        'Digest Size (bytes)',
        choices=[(str(i), f'{i} bytes ({i*8} bits)') for i in [16, 20, 28, 32, 48, 64]],
        default='32',
        validators=[DataRequired()]
    )
    
    blake2_key = StringField(
        'BLAKE2 Key (Optional)',
        validators=[
            Optional(),
            Length(max=64, message='Key must be 64 bytes or less'),
            validate_blake2_key
        ]
    )
    
    blake2_salt = StringField(
        'BLAKE2 Salt (Optional)',
        validators=[
            Optional(),
            Length(max=16, message='Salt must be 16 bytes or less'),
            validate_blake2_salt
        ]
    )
    
    expected_hash = StringField(
        'Expected Hash (for verification)',
        validators=[Optional()],
        render_kw={"placeholder": "Enter the expected hash for verification..."}
    )
    
    submit = SubmitField('Process')

def generate_blake2_hash(text, hash_type, digest_size, key=None, salt=None):
    """Generate BLAKE2 hash with specified parameters"""
    try:
        # Convert inputs to bytes
        text_bytes = text.encode('utf-8')
        digest_size = int(digest_size)
        
        if hash_type in ['blake2b', 'blake2b_keyed']:
            if hash_type == 'blake2b_keyed' and not key:
                raise ValueError("Key is required for keyed BLAKE2b")
            
            if key and salt:
                hasher = hashlib.blake2b(digest_size=digest_size, key=key.encode('utf-8'), salt=salt.encode('utf-8'))
            elif key:
                hasher = hashlib.blake2b(digest_size=digest_size, key=key.encode('utf-8'))
            elif salt:
                hasher = hashlib.blake2b(digest_size=digest_size, salt=salt.encode('utf-8'))
            else:
                hasher = hashlib.blake2b(digest_size=digest_size)
                
        elif hash_type in ['blake2s', 'blake2s_keyed']:
            if hash_type == 'blake2s_keyed' and not key:
                raise ValueError("Key is required for keyed BLAKE2s")
            
            # BLAKE2s max digest size is 32 bytes
            if digest_size > 32:
                digest_size = 32
                
            if key and salt:
                hasher = hashlib.blake2s(digest_size=digest_size, key=key.encode('utf-8'), salt=salt.encode('utf-8'))
            elif key:
                hasher = hashlib.blake2s(digest_size=digest_size, key=key.encode('utf-8'))
            elif salt:
                hasher = hashlib.blake2s(digest_size=digest_size, salt=salt.encode('utf-8'))
            else:
                hasher = hashlib.blake2s(digest_size=digest_size)
        else:
            raise ValueError("Invalid hash type")
        
        hasher.update(text_bytes)
        hash_result = hasher.hexdigest()
        
        return {
            'hash': hash_result,
            'algorithm': hash_type.upper(),
            'digest_size': digest_size,
            'hash_length': len(hash_result),
            'bit_length': digest_size * 8
        }
        
    except Exception as e:
        raise ValueError(f"Hash generation failed: {str(e)}")

def verify_hash_integrity(text, expected_hash, hash_type, digest_size, key=None, salt=None):
    """Verify data integrity by comparing hashes"""
    try:
        # Generate hash with the same parameters
        generated_hash_info = generate_blake2_hash(text, hash_type, digest_size, key, salt)
        generated_hash = generated_hash_info['hash']
        
        # Compare hashes using secure comparison
        is_valid = hmac.compare_digest(generated_hash.lower(), expected_hash.lower())
        
        return {
            'is_valid': is_valid,
            'generated_hash': generated_hash,
            'expected_hash': expected_hash,
            'algorithm': hash_type.upper(),
            'digest_size': digest_size
        }
        
    except Exception as e:
        raise ValueError(f"Hash verification failed: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Blake2Form()
    result = None
    original_text = None
    hash_info = None
    verification_result = None
    
    if form.validate_on_submit():
        try:
            original_text = form.text.data
            
            if form.action.data == 'generate':
                hash_info = generate_blake2_hash(
                    form.text.data,
                    form.hash_type.data,
                    form.blake2_digest_size.data,
                    form.blake2_key.data,
                    form.blake2_salt.data
                )
                result = hash_info['hash']
                flash('Hash generated successfully!', 'success')
                
            elif form.action.data == 'verify':
                if not form.expected_hash.data:
                    flash('Expected hash is required for verification!', 'error')
                else:
                    verification_result = verify_hash_integrity(
                        form.text.data,
                        form.expected_hash.data,
                        form.hash_type.data,
                        form.blake2_digest_size.data,
                        form.blake2_key.data,
                        form.blake2_salt.data
                    )
                    if verification_result['is_valid']:
                        flash('Data integrity verified! Hashes match.', 'success')
                    else:
                        flash('Data integrity failed! Hashes do not match.', 'error')
                        
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    return render_template('index.html', form=form, result=result, 
                         original_text=original_text, hash_info=hash_info, 
                         verification_result=verification_result)

if __name__ == '__main__':
    app.run(debug=True) 