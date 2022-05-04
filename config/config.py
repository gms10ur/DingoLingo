BOT_TOKEN: str = "OTUzNDI2MTgxMDIwMDc4MTEx.YjEZUw.jTtRQFvpI_QFSjfSiBLW0ry_4Z0"
SPOTIFY_ID: str = "1e68c441ccf34d5bba2e497e7e98fbe5"
SPOTIFY_SECRET: str = "85b315143f07466c98bf7bac708fd26a"

BOT_PREFIX = "!"

EMBED_COLOR = 0x2514b8  #replace after'0x' with desired hex code ex. '#ff0188' >> '0xff0188'

SUPPORTED_EXTENSIONS = ('.webm', '.mp4', '.mp3', '.avi', '.wav', '.m4v', '.ogg', '.mov')

MAX_SONG_PRELOAD = 10  #maximum of 25

COOKIE_PATH = "/config/cookies/cookies.txt"

GLOBAL_DISABLE_AUTOJOIN_VC = False

VC_TIMEOUT = 300 #seconds
VC_TIMOUT_DEFAULT = True  #default template setting for VC timeout true= yes, timeout false= no timeout
ALLOW_VC_TIMEOUT_EDIT = True  #allow or disallow editing the vc_timeout guild setting


STARTUP_MESSAGE = "Ritim Show Başlıyor....."
STARTUP_COMPLETE_MESSAGE = "Hazır!"

NO_GUILD_MESSAGE = 'Mekana gitmemişsin henüz, önce sen git sonra beni çağır kral'
USER_NOT_IN_VC_MESSAGE = "Herkesin müziğine kimse karışamaz.."
WRONG_CHANNEL_MESSAGE = "Yanlış yerden bana sesleniyon"
NOT_CONNECTED_MESSAGE = "Beni bi yere çağırmadın ki, !gel de geleyim."
ALREADY_CONNECTED_MESSAGE = "Kral, burdayım zaten"
CHANNEL_NOT_FOUND_MESSAGE = "Yok öyle bi kanal"
DEFAULT_CHANNEL_JOIN_FAILED = "Kanalı kapatmışlar lan!"
INVALID_INVITE_MESSAGE = "Yok öyle bi davet bağlantısı"

ADD_MESSAGE= "Bu botu kendi Sunucunuza eklemek için [buraya] tıklayın" #brackets will be the link text

INFO_HISTORY_TITLE = "Mazide çalınmış şarkılar:"
MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

SONGINFO_UPLOADER = "Kimden: "
SONGINFO_DURATION = "Süresi: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Beğenenler: "
SONGINFO_DISLIKES = "Beğenmeyenler: "
SONGINFO_NOW_PLAYING = "Şimdi çalıyorum gardaş"
SONGINFO_QUEUE_ADDED = "Bi sonra şunu çalcam"
SONGINFO_SONGINFO = "Şarkı bilgisi"
SONGINFO_ERROR = "Senin bunu dinlemeye yaşın yetmiyor gardaşım"
SONGINFO_PLAYLIST_QUEUED = "Bu günkü pileylistimiz :page_with_curl:"
SONGINFO_UNKNOWN_DURATION = "Bilmiyom"

HELP_ADDBOT_SHORT = "Beni başka bi yere davet et"
HELP_ADDBOT_LONG = "Bu botu başka bir sunucunuza eklemeniz için size link verir."
HELP_CONNECT_SHORT = "Botu ses kanalına bağlayın"
HELP_CONNECT_LONG = "Botu şu anda bulunduğunuz ses kanalına bağlar"
HELP_DISCONNECT_SHORT = "Botun ses kanalıyla bağlantısını kes"
HELP_DISCONNECT_LONG = "Botun ses kanalıyla bağlantısını kesin ve sesi durdurun."

HELP_SETTINGS_SHORT = "Ayarlarımla çok oynama"
HELP_SETTINGS_LONG = "Sunucudaki bot ayarlarını görüntüleyin ve ayarlayın. Kullanım: {}settings setting_name value".format(BOT_PREFIX)

HELP_HISTORY_SHORT = "Şarkıların geçmişini göster"
HELP_HISTORY_LONG = "En son çalınan" + str(MAX_TRACKNAME_HISTORY_LENGTH) + " şarkıyı gösterir."
HELP_PAUSE_SHORT = "Müziği Duraklat"
HELP_PAUSE_LONG = "AudioPlayer'ı duraklatır. Devam komutu ile oynatmaya devam edilebilir.."
HELP_VOL_SHORT = "Ses yüksekliğini değiştir %"
HELP_VOL_LONG = "AudioPlayer'ın sesini değiştirir. Değişken, sesin ayarlanması gereken %'yi belirtir."
HELP_PREV_SHORT = "Bir Şarkı geri git"
HELP_PREV_LONG = "Önceki şarkıyı tekrar çalar."
HELP_RESUME_SHORT = "Müzik Devam Et"
HELP_RESUME_LONG = "AudioPlayer'ı sürdürür."
HELP_SKIP_SHORT = "Bir şarkıyı atla"
HELP_SKIP_LONG = "Şu anda çalmakta olan şarkıyı atlar ve sıradaki bir sonraki öğeye gider."
HELP_SONGINFO_SHORT = "Mevcut Şarkı hakkında bilgi"
HELP_SONGINFO_LONG = "Şu anda çalınan şarkıyla ilgili ayrıntıları gösterir ve şarkıya bir bağlantı gönderir."
HELP_STOP_SHORT = "Müziği Durdur"
HELP_STOP_LONG = "AudioPlayer'ı durdurur ve şarkı sırasını temizler"
HELP_MOVE_LONG = f"{BOT_PREFIX}taşı [position] [new position]"
HELP_MOVE_SHORT = 'Kuyruktaki bir parçayı hareket ettirir'
HELP_YT_SHORT = "Desteklenen bir bağlantı oynatın veya youtube'da arama yapın"
HELP_YT_LONG = ("$p [link/video title/key words/playlist-link/soundcloud link/spotify link/bandcamp link/twitter link]")
HELP_PING_SHORT = "Ping"
HELP_PING_LONG = "Botun yanıt durumunu test et"
HELP_CLEAR_SHORT = "Sırayı temizle."
HELP_CLEAR_LONG = "Sırayı temizler ve geçerli şarkıyı atlar."
HELP_LOOP_SHORT = "Şu anda çalmakta olan şarkıyı döngüye sokar, aç/kapat."
HELP_LOOP_LONG = "Şu anda çalmakta olan şarkıyı döngüye alır ve kuyruğu kilitler. Döngüyü devre dışı bırakmak için komutu tekrar kullanın."
HELP_QUEUE_SHORT = "Sıradaki şarkıları gösterir."
HELP_QUEUE_LONG = "10'a kadar sıradaki şarkı sayısını gösterir."
HELP_SHUFFLE_SHORT = "Sırayı karıştır"
HELP_SHUFFLE_LONG = "Geçerli sıradaki şarkıları rastgele sırala"
HELP_CHANGECHANNEL_SHORT = "Bot kanalını değiştir"
HELP_CHANGECHANNEL_LONG = "Bot kanalını bulunduğunuz VC ile değiştirin"

ABSOLUTE_PATH = '' #do not modify