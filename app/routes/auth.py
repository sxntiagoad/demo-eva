from flask import Blueprint, flash, render_template, request, jsonify, redirect, url_for, current_app
from app import db, limiter
from app.forms import RegistrationForm
from app.utils import can_register
from app.models import User
import boto3
from botocore.exceptions import ClientError

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm()

    if form.validate_on_submit():
        ip_address = request.remote_addr
        device_info = request.headers.get('User-Agent')

        if not can_register(ip_address, device_info):
            flash('You have already registered recently. Please try again later.', 'error')
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

            # Generar URL de descarga de S3
            s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
                region_name=current_app.config['AWS_REGION']
            )

            try:
                # Generar URL presignada que expira en 1 hora
                download_url = s3_client.generate_presigned_url('get_object',
                    Params={
                        'Bucket': 'apk-eva',
                        'Key': 'app_release.apk'
                    },
                    ExpiresIn=3600  # URL válida por 1 hora
                )
                return render_template('auth/success.html', token=token, download_url=download_url)
            except ClientError as e:
                current_app.logger.error(f"Error con S3: {str(e)}")
                return render_template('auth/success.html', token=token)

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error durante registro: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', form=form)
