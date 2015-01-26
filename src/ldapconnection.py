__author__ = 'teohoch'
import ldap



def validateLDAP(username,password):
    base_dn = "ou=People,dc=ldapste01,dc=osf,dc=alma,dc=cl"
    ld = ldap.initialize('ldap://ldapste01.osf.alma.cl')
    try:
        ld_username = "uid=" + username + "," + base_dn
        ld.bind_s(ld_username,password)
        result = ld.search_s(base_dn,ldap.SCOPE_SUBTREE,'uid=%s' % (username),['cn','mail'])
        print result
        return True
    except ldap.LDAPError, e:
        print "authentication error"
        print e
        return False

validateLDAP('jreveco','mynewshinypass')