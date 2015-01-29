__author__ = 'teohoch'
import ldap
import simpleldap




def validateLDAP(username,password):
	# ldap://ldapste01.osf.alma.cl
	base_dn = "ou=people,ou=master,dc=alma,dc=info"
	try:
		#Configuraciones para generar la conexion con START_TLS
		ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
		ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,"CAcert.pem")
		ldap.set_option(ldap.OPT_X_TLS_CERTFILE,'support.crt')
		ldap.set_option(ldap.OPT_X_TLS_KEYFILE,'support.key')
		ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

		# Inicializar la conexion
		ld = ldap.initialize('ldap://ldapste01.osf.alma.cl')
		ld.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
		ld.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
		ld.set_option(ldap.OPT_REFERRALS, 1)


		try:
			ld_username = 'uid='+username+',ou=people,ou=master,dc=alma,dc=info'

			# Conectar por START_TLS
			ld.start_tls_s()
			# Ejecutar el Binding, aca deberia decirme cuando la contrasena esta equivocada, pero no los hace
			ld.simple_bind_s(ld_username, password)
			#Imprimo bajo que usuario estoy autentificado
			print ld.whoami_s()
			#Genero un search para que me muestre el usuario
			result = ld.search_s('ou=master,dc=alma,dc=info', ldap.SCOPE_SUBTREE,'uid=%s' % (username))
			return True
		except ldap.LDAPError, e:
			return False
	except:
		raise


ldapsrv = 'ldapste01.osf.alma.cl'
basedn = 'ou=people,ou=master,dc=alma,dc=info'


def ldap_fetch(uid=None, name=None, passwd=None):
    try:
        if name is not None and passwd is not None:
            l = simpleldap.Connection(ldapsrv,
                dn='uid={0},{1}'.format(name, basedn), password=passwd)
            r = l.search('uid={0}'.format(name), base_dn=basedn)
        else:
            l = simpleldap.Connection(ldapsrv)
            r = l.search('uidNumber={0}'.format(uid), base_dn=basedn)

        return {
            'name': r[0]['uid'][0],
            'id': unicode(r[0]['uidNumber'][0]),
            'gid': int(r[0]['gidNumber'][0])
        }
    except Exception as e:
		return None

if __name__ == '__main__':
	print(ldap_fetch(name='jreveco',passwd='mynewsh'))
	print(ldap_fetch(name='jreveco',passwd='mynewshi'))
	print(ldap_fetch(name='jreveco',passwd='amynewshinypass'))
	print(ldap_fetch(name='jreveco',passwd='mynewshinpass123'))

	print validateLDAP('jreveco','mynewsh')
	print validateLDAP('jreveco','mynewshi')
	print validateLDAP('jreveco','amynewshinypass')
	print validateLDAP('jreveco','mynewshinpass123')

