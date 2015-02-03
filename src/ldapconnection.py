__author__ = 'teohoch'
import ldap

def validateLDAP(uid=None,username=None,password=None):
	# ldap://ldapste01.osf.alma.cl
	base_dn = "ou=people,ou=master,dc=alma,dc=info"
	uri = 'ldap://ldapste01.osf.alma.cl'
	try:
		#Configs for a START_TLS connection
		ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
		ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,"CAcert.pem")
		ldap.set_option(ldap.OPT_X_TLS_CERTFILE,'support.crt')
		ldap.set_option(ldap.OPT_X_TLS_KEYFILE,'support.key')
		ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

		# initialize the connection
		ld = ldap.initialize(uri)
		ld.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
		ld.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
		ld.set_option(ldap.OPT_REFERRALS, 1)

		if username is not None and password is not None:
			try:

				# Ejecutar el Binding, aca deberia decirme cuando la contrasena esta equivocada, pero no los hace
				ld.simple_bind_s('uid='+username+','+base_dn, password)
				#Imprimo bajo que usuario estoy autentificado
				#print ld.whoami_s()
				#Genero un search para que me muestre el usuario
				r = ld.search_s(base_dn, ldap.SCOPE_SUBTREE,'uid=%s' % (username))

			except ldap.LDAPError, e:
				print e
				return None
		else:
			try:
				ld.simple_bind_s()
				r = ld.search_s(base_dn, ldap.SCOPE_SUBTREE,'uidNumber=%s' % (uid))
			except Exception as e:
				print e
				return None
		return {
            'username': r[0][1]['uid'][0],
            'name': r[0][1]['cn'][0],
            'id': unicode(r[0][1]['uidNumber'][0]),
            'gid': int(r[0][1]['gidNumber'][0])
        }
	except:
		return None

if __name__ == '__main__':


	print validateLDAP_test(username="jreveco",password="mynewshinypass")
	print validateLDAP_test(uid='1124')

