import logging
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings


def validate_email_domain_restriction(value):
    logging.info('Checking email domain in preset domains..')
    valid_domains = []
    validation_result = {}
    try:
        email_domain = value.split('@')[1]
        valid_domains = [settings.LDAP_DOMAIN_MAIL]
    except AttributeError, e:
        logging.warning("Email domain verification is omitted. %s", e)
    except Exception, e:
        logging.warning("Email domain verification failed. %s", e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    
    if email_domain not in valid_domains:
        logging.warning("Invalid email domain {}, valid are {}"
                        .format(email_domain, valid_domains))
        validation_result.update({'field':'email',
                                  'message': _('email_domain_restriction')})
    return validation_result
