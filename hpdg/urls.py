from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("", views.home, name="home"),
   #  path("inscription_c", views.inscription_c, name="inscription"),
   #  path("connexion_c", views.connexion_c, name="connexion"),
   #  path("consulter_dispo", views.consulter_dispo, name="consulter_dispo"),
   #  path("effectuer_reservation", views.effectuer_reservation, name="effectuer_reservation"),
   #  path("connexion_a", views.connexion_a, name="connexion_a"),
   #  path("inscription_a", views.inscription_a, name="inscription_a"),
   #  path("profil_c", views.profil_c, name="profil_c"),
   #  path("profil_a", views.profil_a, name="profil_a"),
   #  path("home_a", views.home_a, name="home_a"),
   #  path("home_sp", views.home_sp, name="home_sp"),
   #  path("chat/<str:chat_box_name>/", views.chat_box, name="chat"),
   #  path("download", views.downloadPage, name="Download"),
   #  path("uploadimage", views.upload_image, name="upload-image"),
    
    
    path("user/token/add", views.createToken, name="create-user-token"),
    path("token", views.refreshToken, name="login"),
    path("token/setpassword", views.setPassword, name="setpassword"),
    path("token/logout", views.signOut, name="logout"),
    path("token/verify", views.verifyToken, name="verify-token"),
    
    path("client/add", views.createClient, name="add-client"),
    path("client/set", views.updateClient, name="set-client"),
    #path("client/setpassword", views.updateUserPassword, name="set-clientpassword"),
    path("client/get", views.getClient, name="get-client"),
    #path("client/verifyregistration", views.getClientInscriptionState, name="get-client-registration"),
    path("client/getwithemailandpwd", views.getClientWithEmailandPwd, name="get-clientwithemail"),
    path("client/delete", views.deleteClient, name="delete-client"),
    path("clients/delete", views.deleteClients, name="delete-clients"),
    

    path("admin/add", views.createAdmin, name="add-admin"),
    path("admin/set", views.updateAdmin, name="set-admin"),
    #path("admin/setpassword", views.updateUserPassword, name="set-adminpassword"),
    path("admin/get", views.getAdmin, name="get-admin"),
    #path("admin/verifyregistration", views.getadminInscriptionState, name="get-admin-registration"),
    path("admin/getwithemailandpwd", views.getAdminWithEmailandPwd, name="get-adminwithemail"),
    path("admin/delete", views.deleteAdmin, name="delete-admin"),
   # path("admins/delete", views.deleteAdmins, name="delete-admins"),

   path("superadmin/add", views.createSuperadmin, name="add-superadmin"),
    path("superadmin/set", views.updateSuperadmin, name="set-superadmin"),
    #path("superadmin/setpassword", views.updateUserPassword, name="set-superadminpassword"),
    path("superadmin/get", views.getSuperadmin, name="get-superadmin"),
    #path("superadmin/verifyregistration", views.getsuperadminInscriptionState, name="get-superadmin-registration"),
    path("superadmin/getwithemailandpwd", views.getSuperadminWithEmailandPwd, name="get-superadminwithemail"),
    path("superadmin/delete", views.deleteSuperadmin, name="delete-superadmin"),
    path("superadmins/delete", views.deleteSuperadmins, name="delete-superadmins"),

    path("entite/add", views.createEntite, name="add-entite"),
    path("entite/set", views.updateEntite, name="set-entite"),
    #path("entite/setpassword", views.updateUserPassword, name="set-entitepassword"),
    path("entite/get", views.getEntite, name="get-entite"),
    #path("entite/verifyregistration", views.getentiteInscriptionState, name="get-entite-registration"),
    path("entite/getwithemailandpwd", views.getEntiteWithEmailandPwd, name="get-entitewithemail"),
    path("entite/delete", views.deleteEntite, name="delete-entite"),
   # path("entites/delete", views.deleteentites, name="delete-entites"),

    path("reservation/add", views.createReservation, name="add-reservation"),
    path("reservation/set", views.updateReservation, name="set-reservation"),
    path("reservation/get", views.getReservation, name="get-reservation"),
    path("reservations/get", views.getReservations, name="get-reservations"),
    path("entite/reservations/get", views.getReservationsFromEntity, name="get-reservations-entite"),
    path("reservation/delete", views.deleteReservation, name="delete-reservation"),
   #  path("reservations/delete", views.deleteReservations, name="delete-reservations"),

    path("chambre/add", views.createChambre, name="add-chambre"),
    path("chambre/set", views.updateChambre, name="set-chambre"),
    path("chambre/get", views.getChambre, name="get-chambre"),
    path("chambres/get", views.getChambres, name="get-chambres"),
    path("entite/chambres/get", views.getChambresFromEntity, name="get-chambres-entite"),
    path("chambre/delete", views.deleteChambre, name="delete-chambre"),
   #  path("chambres/delete", views.deleteChambres, name="delete-reservations"),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
