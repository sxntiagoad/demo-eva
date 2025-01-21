from flask import Blueprint, flash, render_template, request, jsonify, redirect, url_for, current_app
from app import db, limiter
from app.forms import RegistrationForm
from app.utils import can_register
from app.models import User
import boto3
from botocore.exceptions import ClientError
import os

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm()

    if form.validate_on_submit():
        ip_address = request.remote_addr
        device_info = request.headers.get('User-Agent')

        if not can_register(ip_address, device_info):
            flash('Te registraste recientemente. Por favor, inténtalo de nuevo más tarde.', 'error')
            return redirect(url_for('auth.register'))
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            ip_address=ip_address,
            device_info=device_info
        )
        try:
            db.session.add(user)
            db.session.commit()
            token = user.generate_token()
            db.session.commit()

            try:
                session = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')
                )
                
                s3_client = session.client('s3')
                
                # Generar URL presignada con Content-Disposition
                download_url = s3_client.generate_presigned_url('get_object',
                    Params={
                        'Bucket': os.getenv('AWS_BUCKET_NAME', 'apk-eva'),
                        'Key': 'app-release.apk',
                        'ResponseContentDisposition': 'attachment; filename="app-release.apk"'
                    },
                    ExpiresIn=3600
                )
                
                current_app.logger.info(f"URL de descarga generada: {download_url}")
                return render_template('auth/success.html', token=token, download_url=download_url)
                
            except Exception as e:
                current_app.logger.error(f"Error con S3: {str(e)}")
                return render_template('auth/success.html', token=token)

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error durante registro: {str(e)}")
            flash('Un error ocurrió durante el registro. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/api/verify-token', methods=['POST'])
def verify_token():
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Se requiere contenido JSON'
            }), 400

        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({
                'success': False,
                'error': 'Token no proporcionado'
            }), 400

        token = data['token']
        user = User.verify_token(token)  # Usando el nuevo método

        if not user:
            return jsonify({
                'success': False,
                'error': 'Token inválido o expirado'
            }), 401

        return jsonify({
            'success': True,
            'message': 'Token válido',
            'data': user.to_dict()  # Usando el nuevo método
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error verificando token: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
