# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alternativetitles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    title = models.TextField(db_column='Title')  # Field name made lowercase.
    cleantitle = models.TextField(db_column='CleanTitle', unique=True)  # Field name made lowercase.
    sourcetype = models.IntegerField(db_column='SourceType')  # Field name made lowercase.
    sourceid = models.IntegerField(db_column='SourceId')  # Field name made lowercase.
    votes = models.IntegerField(db_column='Votes')  # Field name made lowercase.
    votecount = models.IntegerField(db_column='VoteCount')  # Field name made lowercase.
    language = models.IntegerField(db_column='Language')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AlternativeTitles'


class Blacklist(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    sourcetitle = models.TextField(db_column='SourceTitle')  # Field name made lowercase.
    quality = models.TextField(db_column='Quality')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    publisheddate = models.DateTimeField(db_column='PublishedDate', blank=True, null=True)  # Field name made lowercase.
    size = models.IntegerField(db_column='Size', blank=True, null=True)  # Field name made lowercase.
    protocol = models.IntegerField(db_column='Protocol', blank=True, null=True)  # Field name made lowercase.
    indexer = models.TextField(db_column='Indexer', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    torrentinfohash = models.TextField(db_column='TorrentInfoHash', blank=True, null=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Blacklist'


class Commands(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    body = models.TextField(db_column='Body')  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    queuedat = models.DateTimeField(db_column='QueuedAt')  # Field name made lowercase.
    startedat = models.DateTimeField(db_column='StartedAt', blank=True, null=True)  # Field name made lowercase.
    endedat = models.DateTimeField(db_column='EndedAt', blank=True, null=True)  # Field name made lowercase.
    duration = models.TextField(db_column='Duration', blank=True, null=True)  # Field name made lowercase.
    exception = models.TextField(db_column='Exception', blank=True, null=True)  # Field name made lowercase.
    trigger = models.IntegerField(db_column='Trigger')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Commands'


class Config(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    key = models.TextField(db_column='Key', unique=True)  # Field name made lowercase.
    value = models.TextField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Config'


class Delayprofiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    enableusenet = models.IntegerField(db_column='EnableUsenet')  # Field name made lowercase.
    enabletorrent = models.IntegerField(db_column='EnableTorrent')  # Field name made lowercase.
    preferredprotocol = models.IntegerField(db_column='PreferredProtocol')  # Field name made lowercase.
    usenetdelay = models.IntegerField(db_column='UsenetDelay')  # Field name made lowercase.
    torrentdelay = models.IntegerField(db_column='TorrentDelay')  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    tags = models.TextField(db_column='Tags')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DelayProfiles'


class Downloadclients(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    enable = models.IntegerField(db_column='Enable')  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    implementation = models.TextField(db_column='Implementation')  # Field name made lowercase.
    settings = models.TextField(db_column='Settings')  # Field name made lowercase.
    configcontract = models.TextField(db_column='ConfigContract')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DownloadClients'


class Extrafiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    moviefileid = models.IntegerField(db_column='MovieFileId')  # Field name made lowercase.
    relativepath = models.TextField(db_column='RelativePath')  # Field name made lowercase.
    extension = models.TextField(db_column='Extension')  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added')  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExtraFiles'


class History(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    sourcetitle = models.TextField(db_column='SourceTitle')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    quality = models.TextField(db_column='Quality')  # Field name made lowercase.
    data = models.TextField(db_column='Data')  # Field name made lowercase.
    eventtype = models.IntegerField(db_column='EventType', blank=True, null=True)  # Field name made lowercase.
    downloadid = models.TextField(db_column='DownloadId', blank=True, null=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'History'


class Importexclusions(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    tmdbid = models.IntegerField(db_column='TmdbId', unique=True)  # Field name made lowercase.
    movietitle = models.TextField(db_column='MovieTitle', blank=True, null=True)  # Field name made lowercase.
    movieyear = models.IntegerField(db_column='MovieYear', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ImportExclusions'


class Indexerstatus(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    indexerid = models.IntegerField(db_column='IndexerId', unique=True)  # Field name made lowercase.
    initialfailure = models.DateTimeField(db_column='InitialFailure', blank=True, null=True)  # Field name made lowercase.
    mostrecentfailure = models.DateTimeField(db_column='MostRecentFailure', blank=True, null=True)  # Field name made lowercase.
    escalationlevel = models.IntegerField(db_column='EscalationLevel')  # Field name made lowercase.
    disabledtill = models.DateTimeField(db_column='DisabledTill', blank=True, null=True)  # Field name made lowercase.
    lastrsssyncreleaseinfo = models.TextField(db_column='LastRssSyncReleaseInfo', blank=True, null=True)  # Field name made lowercase.
    cookies = models.TextField(db_column='Cookies', blank=True, null=True)  # Field name made lowercase.
    cookiesexpirationdate = models.DateTimeField(db_column='CookiesExpirationDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IndexerStatus'


class Indexers(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', unique=True)  # Field name made lowercase.
    implementation = models.TextField(db_column='Implementation')  # Field name made lowercase.
    settings = models.TextField(db_column='Settings', blank=True, null=True)  # Field name made lowercase.
    configcontract = models.TextField(db_column='ConfigContract', blank=True, null=True)  # Field name made lowercase.
    enablerss = models.IntegerField(db_column='EnableRss', blank=True, null=True)  # Field name made lowercase.
    enablesearch = models.IntegerField(db_column='EnableSearch', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Indexers'


class Metadata(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    enable = models.IntegerField(db_column='Enable')  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    implementation = models.TextField(db_column='Implementation')  # Field name made lowercase.
    settings = models.TextField(db_column='Settings')  # Field name made lowercase.
    configcontract = models.TextField(db_column='ConfigContract')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Metadata'


class Metadatafiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    consumer = models.TextField(db_column='Consumer')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    relativepath = models.TextField(db_column='RelativePath')  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated')  # Field name made lowercase.
    moviefileid = models.IntegerField(db_column='MovieFileId', blank=True, null=True)  # Field name made lowercase.
    hash = models.TextField(db_column='Hash', blank=True, null=True)  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added', blank=True, null=True)  # Field name made lowercase.
    extension = models.TextField(db_column='Extension')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MetadataFiles'


class Moviefiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    path = models.TextField(db_column='Path', unique=True, blank=True, null=True)  # Field name made lowercase.
    quality = models.TextField(db_column='Quality')  # Field name made lowercase.
    size = models.IntegerField(db_column='Size')  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='DateAdded')  # Field name made lowercase.
    scenename = models.TextField(db_column='SceneName', blank=True, null=True)  # Field name made lowercase.
    mediainfo = models.TextField(db_column='MediaInfo', blank=True, null=True)  # Field name made lowercase.
    releasegroup = models.TextField(db_column='ReleaseGroup', blank=True, null=True)  # Field name made lowercase.
    relativepath = models.TextField(db_column='RelativePath', blank=True, null=True)  # Field name made lowercase.
    edition = models.TextField(db_column='Edition', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MovieFiles'


class Movies(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    imdbid = models.TextField(db_column='ImdbId', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title')  # Field name made lowercase.
    titleslug = models.TextField(db_column='TitleSlug', unique=True)  # Field name made lowercase.
    sorttitle = models.TextField(db_column='SortTitle', blank=True, null=True)  # Field name made lowercase.
    cleantitle = models.TextField(db_column='CleanTitle')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    overview = models.TextField(db_column='Overview', blank=True, null=True)  # Field name made lowercase.
    images = models.TextField(db_column='Images')  # Field name made lowercase.
    path = models.TextField(db_column='Path')  # Field name made lowercase.
    monitored = models.IntegerField(db_column='Monitored')  # Field name made lowercase.
    profileid = models.IntegerField(db_column='ProfileId')  # Field name made lowercase.
    lastinfosync = models.DateTimeField(db_column='LastInfoSync', blank=True, null=True)  # Field name made lowercase.
    lastdisksync = models.DateTimeField(db_column='LastDiskSync', blank=True, null=True)  # Field name made lowercase.
    runtime = models.IntegerField(db_column='Runtime')  # Field name made lowercase.
    incinemas = models.DateTimeField(db_column='InCinemas', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added', blank=True, null=True)  # Field name made lowercase.
    actors = models.TextField(db_column='Actors', blank=True, null=True)  # Field name made lowercase.
    ratings = models.TextField(db_column='Ratings', blank=True, null=True)  # Field name made lowercase.
    genres = models.TextField(db_column='Genres', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)  # Field name made lowercase.
    certification = models.TextField(db_column='Certification', blank=True, null=True)  # Field name made lowercase.
    addoptions = models.TextField(db_column='AddOptions', blank=True, null=True)  # Field name made lowercase.
    moviefileid = models.IntegerField(db_column='MovieFileId')  # Field name made lowercase.
    tmdbid = models.IntegerField(db_column='TmdbId')  # Field name made lowercase.
    website = models.TextField(db_column='Website', blank=True, null=True)  # Field name made lowercase.
    physicalrelease = models.DateTimeField(db_column='PhysicalRelease', blank=True, null=True)  # Field name made lowercase.
    youtubetrailerid = models.TextField(db_column='YouTubeTrailerId', blank=True, null=True)  # Field name made lowercase.
    studio = models.TextField(db_column='Studio', blank=True, null=True)  # Field name made lowercase.
    minimumavailability = models.IntegerField(db_column='MinimumAvailability')  # Field name made lowercase.
    haspredbentry = models.IntegerField(db_column='HasPreDBEntry')  # Field name made lowercase.
    pathstate = models.IntegerField(db_column='PathState')  # Field name made lowercase.
    physicalreleasenote = models.TextField(db_column='PhysicalReleaseNote', blank=True, null=True)  # Field name made lowercase.
    secondaryyear = models.IntegerField(db_column='SecondaryYear', blank=True, null=True)  # Field name made lowercase.
    secondaryyearsourceid = models.IntegerField(db_column='SecondaryYearSourceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Movies'


class Namingconfig(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    multiepisodestyle = models.IntegerField(db_column='MultiEpisodeStyle')  # Field name made lowercase.
    renameepisodes = models.IntegerField(db_column='RenameEpisodes', blank=True, null=True)  # Field name made lowercase.
    replaceillegalcharacters = models.IntegerField(db_column='ReplaceIllegalCharacters')  # Field name made lowercase.
    standardmovieformat = models.TextField(db_column='StandardMovieFormat', blank=True, null=True)  # Field name made lowercase.
    moviefolderformat = models.TextField(db_column='MovieFolderFormat', blank=True, null=True)  # Field name made lowercase.
    colonreplacementformat = models.IntegerField(db_column='ColonReplacementFormat')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NamingConfig'


class Netimport(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='Enabled')  # Field name made lowercase.
    name = models.TextField(db_column='Name', unique=True)  # Field name made lowercase.
    implementation = models.TextField(db_column='Implementation')  # Field name made lowercase.
    configcontract = models.TextField(db_column='ConfigContract', blank=True, null=True)  # Field name made lowercase.
    settings = models.TextField(db_column='Settings', blank=True, null=True)  # Field name made lowercase.
    enableauto = models.IntegerField(db_column='EnableAuto')  # Field name made lowercase.
    rootfolderpath = models.TextField(db_column='RootFolderPath')  # Field name made lowercase.
    shouldmonitor = models.IntegerField(db_column='ShouldMonitor')  # Field name made lowercase.
    profileid = models.IntegerField(db_column='ProfileId')  # Field name made lowercase.
    minimumavailability = models.IntegerField(db_column='MinimumAvailability')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NetImport'


class Notifications(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    ongrab = models.IntegerField(db_column='OnGrab')  # Field name made lowercase.
    ondownload = models.IntegerField(db_column='OnDownload')  # Field name made lowercase.
    settings = models.TextField(db_column='Settings')  # Field name made lowercase.
    implementation = models.TextField(db_column='Implementation')  # Field name made lowercase.
    configcontract = models.TextField(db_column='ConfigContract', blank=True, null=True)  # Field name made lowercase.
    onupgrade = models.IntegerField(db_column='OnUpgrade', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)  # Field name made lowercase.
    onrename = models.IntegerField(db_column='OnRename')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notifications'


class Pendingreleases(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title')  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added')  # Field name made lowercase.
    release = models.TextField(db_column='Release')  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    parsedmovieinfo = models.TextField(db_column='ParsedMovieInfo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PendingReleases'


class Profiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', unique=True)  # Field name made lowercase.
    cutoff = models.IntegerField(db_column='Cutoff')  # Field name made lowercase.
    items = models.TextField(db_column='Items')  # Field name made lowercase.
    language = models.IntegerField(db_column='Language', blank=True, null=True)  # Field name made lowercase.
    preferredtags = models.TextField(db_column='PreferredTags', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Profiles'


class Qualitydefinitions(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    quality = models.IntegerField(db_column='Quality', unique=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', unique=True)  # Field name made lowercase.
    minsize = models.TextField(db_column='MinSize', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    maxsize = models.TextField(db_column='MaxSize', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'QualityDefinitions'


class Remotepathmappings(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    host = models.TextField(db_column='Host')  # Field name made lowercase.
    remotepath = models.TextField(db_column='RemotePath')  # Field name made lowercase.
    localpath = models.TextField(db_column='LocalPath')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemotePathMappings'


class Restrictions(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    required = models.TextField(db_column='Required', blank=True, null=True)  # Field name made lowercase.
    preferred = models.TextField(db_column='Preferred', blank=True, null=True)  # Field name made lowercase.
    ignored = models.TextField(db_column='Ignored', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(db_column='Tags')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Restrictions'


class Rootfolders(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    path = models.TextField(db_column='Path', unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RootFolders'


class Scheduledtasks(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    typename = models.TextField(db_column='TypeName', unique=True)  # Field name made lowercase.
    interval = models.TextField(db_column='Interval')  # Field name made lowercase. This field type is a guess.
    lastexecution = models.DateTimeField(db_column='LastExecution')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ScheduledTasks'


class Subtitlefiles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    movieid = models.IntegerField(db_column='MovieId')  # Field name made lowercase.
    moviefileid = models.IntegerField(db_column='MovieFileId')  # Field name made lowercase.
    relativepath = models.TextField(db_column='RelativePath')  # Field name made lowercase.
    extension = models.TextField(db_column='Extension')  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added')  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated')  # Field name made lowercase.
    language = models.IntegerField(db_column='Language')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubtitleFiles'


class Tags(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    label = models.TextField(db_column='Label', unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tags'


class Users(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    identifier = models.TextField(db_column='Identifier', unique=True)  # Field name made lowercase.
    username = models.TextField(db_column='Username', unique=True)  # Field name made lowercase.
    password = models.TextField(db_column='Password')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'


class Versioninfo(models.Model):
    version = models.IntegerField(db_column='Version', unique=True)  # Field name made lowercase.
    appliedon = models.DateTimeField(db_column='AppliedOn', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VersionInfo'
