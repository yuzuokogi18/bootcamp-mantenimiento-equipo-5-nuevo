CREATE DATABASE IF NOT EXISTS broken_tunes;
USE broken_tunes;


CREATE TABLE IF NOT EXISTS artists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS songs_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    artist_id INT,
    mp3_data LONGBLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);


CREATE OR REPLACE VIEW songs AS
SELECT 
    s.id, 
    s.title, 
    a.name AS artist, 
    s.mp3_data, 
    s.created_at
FROM songs_data s
LEFT JOIN artists a ON s.artist_id = a.id;


CREATE TABLE IF NOT EXISTS songs_backup (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_song_id INT NULL,
    title VARCHAR(200) NOT NULL,
    artist VARCHAR(200) NOT NULL, 
    mp3_data LONGBLOB,
    backup_note VARCHAR(255) DEFAULT 'periodic backup',
    backed_up_by VARCHAR(100) DEFAULT 'system',
    backed_up_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS file_index (
  id INT AUTO_INCREMENT PRIMARY KEY,
  song_id INT NULL,
  file_path VARCHAR(500) DEFAULT NULL,
  mp3_data LONGBLOB,
  note VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DELIMITER //

CREATE PROCEDURE sp_insert_song(IN p_title VARCHAR(200), IN p_artist_name VARCHAR(200), IN p_data LONGBLOB)
BEGIN
    DECLARE v_artist_id INT;
    INSERT IGNORE INTO artists (name) VALUES (p_artist_name);
    SELECT id INTO v_artist_id FROM artists WHERE name = p_artist_name LIMIT 1;
    INSERT INTO songs_data (title, artist_id, mp3_data) VALUES (p_title, v_artist_id, p_data);
END//

DELIMITER ;

INSERT INTO users (username, password) VALUES ('admin', '1234'), ('user', 'password');

CALL sp_insert_song('Test Song', 'Broken Band', FROM_BASE64('U29tZQ=='));
CALL sp_insert_song('Sunny Day', 'Lazy Artist', FROM_BASE64('QXVkaW8='));
CALL sp_insert_song('Night Drive', 'Neon Roads', FROM_BASE64('VGVzdA=='));
CALL sp_insert_song('Coffee Break', 'Minimalista', FROM_BASE64('QmFzZTY0'));
CALL sp_insert_song('Rainy Window', 'LoFi Beats', FROM_BASE64('Q2xpcA=='));
CALL sp_insert_song('Short Clip', 'Clip Band', FROM_BASE64('TW9jaw=='));
CALL sp_insert_song('Ambient Space', 'Drift', FROM_BASE64('U2hvcnQ='));
CALL sp_insert_song('Tiny Loop', 'Loopers', FROM_BASE64('QmVhdA=='));
CALL sp_insert_song('Base64 Jam', 'Encoderz', FROM_BASE64('QXVkaW8x'));
CALL sp_insert_song('Duplicate Title', 'Echoes', FROM_BASE64('QXVkaW8y'));
CALL sp_insert_song('Duplicate Title', 'Echoes', FROM_BASE64('QXVkaW8z'));
CALL sp_insert_song('Remix One', 'DJ Test', FROM_BASE64('UmVtaXg='));
CALL sp_insert_song('Remix One', 'DJ Test', FROM_BASE64('UmVtaXgy'));
CALL sp_insert_song('Track 01', 'Factory', FROM_BASE64('VHJhY2sx'));
CALL sp_insert_song('Track 02', 'Factory', FROM_BASE64('VHJhY2sy'));
CALL sp_insert_song('Loop 1', 'Loopers', FROM_BASE64('TG9vcDE='));
CALL sp_insert_song('Loop 2', 'Loopers', FROM_BASE64('TG9vcDI='));
CALL sp_insert_song('Sunny Day (Acoustic)', 'Lazy Artist', FROM_BASE64('U3Vubnk='));
CALL sp_insert_song('Overshot', 'Neon Roads', FROM_BASE64('T3ZlcnM='));
CALL sp_insert_song('Coffee Break (Short)', 'Minimalista', FROM_BASE64('Q29mZg=='));
CALL sp_insert_song('Rainy Window (Edit)', 'LoFi Beats', FROM_BASE64('UmFpbg=='));
CALL sp_insert_song('Tiny Loop (v2)', 'Loopers', FROM_BASE64('VHYy'));
CALL sp_insert_song('Ambient Space - Extended', 'Drift', FROM_BASE64('RXh0ZW5k'));
CALL sp_insert_song('Base64 Jam - Live', 'Encoderz', FROM_BASE64('TGl2ZQ=='));
CALL sp_insert_song('Clip One', 'Clip Band', FROM_BASE64('Q2xpcDE='));
CALL sp_insert_song('Clip Two', 'Clip Band', FROM_BASE64('Q2xpcDI='));
CALL sp_insert_song('Echo Chamber', 'Echoes', FROM_BASE64('RWNobw=='));
CALL sp_insert_song('Broken Loop', 'Broken Band', FROM_BASE64('QnJva2Vu'));
CALL sp_insert_song('Neon Drive (Remastered)', 'Neon Roads', FROM_BASE64('UmVtYXN0'));
CALL sp_insert_song('Duplicate Artist', 'Lazy Artist', FROM_BASE64('RHVwbA=='));
CALL sp_insert_song('Weird Name 1', 'Strange/Artist<>', FROM_BASE64('V2VpcmQ='));
CALL sp_insert_song('Weird Name 2', 'Strange/Artist<>', FROM_BASE64('V2VpcmQy'));
CALL sp_insert_song('Single', 'Soloist', FROM_BASE64('U2luZ2xl'));
CALL sp_insert_song('Double', 'Twin', FROM_BASE64('RHViYmxl'));
CALL sp_insert_song('BSide', 'Oldies', FROM_BASE64('QlNpZGU='));
CALL sp_insert_song('Hidden Track', 'Various', FROM_BASE64('SGlkZGVu'));
CALL sp_insert_song('Live 2019', 'StageBand', FROM_BASE64('TGl2ZTE5'));
CALL sp_insert_song('Live 2020', 'StageBand', FROM_BASE64('TGl2ZTIw'));
CALL sp_insert_song('Collab One', 'Artist A & Artist B', FROM_BASE64('Q29sbGFiMQ=='));
CALL sp_insert_song('Collab Two', 'Artist A & Artist B', FROM_BASE64('Q29sbGFiMg=='));
CALL sp_insert_song('Reprise', 'Composer', FROM_BASE64('UmVwcmlzZQ=='));
CALL sp_insert_song('Interlude', 'Composer', FROM_BASE64('SW50ZXJs'));
CALL sp_insert_song('Outro', 'Finale', FROM_BASE64('T3V0cm8='));
CALL sp_insert_song('Intro', 'Prelude', FROM_BASE64('SW50cm8='));
CALL sp_insert_song('Loop Short', 'Loopers', FROM_BASE64('TG9vc1M='));
CALL sp_insert_song('Loop Long', 'Loopers', FROM_BASE64('TG9vc0xvZw=='));
CALL sp_insert_song('Cheap Sample', 'Sampler', FROM_BASE64('U2FtcGxl'));
CALL sp_insert_song('Debug Tone', 'TestLab', FROM_BASE64('RGVidWc='));
CALL sp_insert_song('Mixdown 1', 'Studio', FROM_BASE64('TWl4MQ=='));
CALL sp_insert_song('Mixdown 2', 'Studio', FROM_BASE64('TWl4Mg=='));
CALL sp_insert_song('Snippet A', 'Editor', FROM_BASE64('U25pcA=='));
CALL sp_insert_song('Snippet B', 'Editor', FROM_BASE64('U25pcGI='));
CALL sp_insert_song('One Minute', 'Shorts', FROM_BASE64('T25lTWlu'));
CALL sp_insert_song('Two Minutes', 'Shorts', FROM_BASE64('VHdvTWlu'));
CALL sp_insert_song('Ambient 1', 'Drift', FROM_BASE64('QW1iaWVy'));
CALL sp_insert_song('Ambient 2', 'Drift', FROM_BASE64('QW1iaWVyMg=='));
CALL sp_insert_song('Field Recording', 'Field', FROM_BASE64('RmllbGQ='));
CALL sp_insert_song('Sampler Pack', 'Various', FROM_BASE64('U2FtcA=='));
CALL sp_insert_song('Test Clip 1', 'QA', FROM_BASE64('VGVzdDE='));
CALL sp_insert_song('Test Clip 2', 'QA', FROM_BASE64('VGVzdDI='));
CALL sp_insert_song('Alpha', 'Beta', FROM_BASE64('QWxwaGE='));
CALL sp_insert_song('Beta', 'Beta', FROM_BASE64('QmV0YQ=='));
CALL sp_insert_song('Gamma', 'Beta', FROM_BASE64('R2FtbWE='));
CALL sp_insert_song('Delta', 'Beta', FROM_BASE64('RGVsdGE='));
CALL sp_insert_song('Epsilon', 'Beta', FROM_BASE64('RXBzaWxvbg=='));
CALL sp_insert_song('Zeta', 'Beta', FROM_BASE64('WmV0YQ=='));
CALL sp_insert_song('Eta', 'Beta', FROM_BASE64('RXRh'));
CALL sp_insert_song('Theta', 'Beta', FROM_BASE64('VGhldGE='));
CALL sp_insert_song('Iota', 'Beta', FROM_BASE64('SW90YQ=='));
CALL sp_insert_song('Kappa', 'Beta', FROM_BASE64('S2FwcGE='));
CALL sp_insert_song('Long Name with many words to make things messy and test display', 'Verbose Artist', FROM_BASE64('TG9uZ05hbWU='));
CALL sp_insert_song('Special & Chars !@#$', 'Punctuated', FROM_BASE64('U3BlY2lhbA=='));
CALL sp_insert_song('Bracket [Test]', 'Brackets', FROM_BASE64('QnJhY2tldA=='));
CALL sp_insert_song('Slash/Backslash\\Test', 'Slasher', FROM_BASE64('U2xhc2hlcg=='));
CALL sp_insert_song('Comma,Separated,Name', 'CSV Band', FROM_BASE64('Q1NW'));
CALL sp_insert_song('Tab\tName', 'Whitespace', FROM_BASE64('V2hpdGVzcGFjZQ=='));
CALL sp_insert_song('New\nLine', 'Whitespace', FROM_BASE64('TmV3TGluZQ=='));
CALL sp_insert_song('Emoji 🙂', 'Icons', FROM_BASE64('RW1vamk='));
CALL sp_insert_song('Duplicate 1', 'Dupers', FROM_BASE64('RHVwMQ=='));
CALL sp_insert_song('Duplicate 1', 'Dupers', FROM_BASE64('RHVwMg=='));
CALL sp_insert_song('Duplicate 2', 'Dupers', FROM_BASE64('RHVwMw=='));
CALL sp_insert_song('Spam Track', 'Noise', FROM_BASE64('U3BhbQ=='));
CALL sp_insert_song('Noise 1', 'Noise', FROM_BASE64('Tm9pc2Ux'));
CALL sp_insert_song('Noise 2', 'Noise', FROM_BASE64('Tm9pc2Uy'));
CALL sp_insert_song('Glitch A', 'Glitchers', FROM_BASE64('R2xpdGNoQQ=='));
CALL sp_insert_song('Glitch B', 'Glitchers', FROM_BASE64('R2xpdGNoQg=='));
CALL sp_insert_song('Test-123', 'Numbers', FROM_BASE64('VGVzdC0xMjM='));
CALL sp_insert_song('Track_underscore', 'UnderScore', FROM_BASE64('VHJhY2tf'));
CALL sp_insert_song('Lowercase', 'artistlower', FROM_BASE64('bG93ZXI='));
CALL sp_insert_song('UPPERCASE', 'ARTISTUP', FROM_BASE64('VVBF'));
CALL sp_insert_song('MiXeDCase', 'ArtistMix', FROM_BASE64('TWl4Q2FzZQ=='));
CALL sp_insert_song('Spaces    Multiple', 'Spacing', FROM_BASE64('U3BhY2luZw=='));
CALL sp_insert_song('TrailingSpace ', 'Trim', FROM_BASE64('VHJpbQ=='));
CALL sp_insert_song('LeadingSpace', ' Trim', FROM_BASE64('TGVhZA=='));
CALL sp_insert_song('VeryVeryLongTitle_' , 'LongArtistName_WhichIsAlsoQuiteLongToTestColumns', FROM_BASE64('TG9uZ1RpdGxl'));
CALL sp_insert_song('Short', 'S', FROM_BASE64('U2hvcnQ='));
CALL sp_insert_song('A', 'B', FROM_BASE64('QQ=='));
CALL sp_insert_song('B', 'A', FROM_BASE64('Qg=='));
CALL sp_insert_song('Orphan', 'NoArtist', FROM_BASE64('T3JwaGFu'));
CALL sp_insert_song('Catalog 001', 'Catalog', FROM_BASE64('Q2F0YTE='));
CALL sp_insert_song('Catalog 002', 'Catalog', FROM_BASE64('Q2F0YTI='));
CALL sp_insert_song('Catalog 003', 'Catalog', FROM_BASE64('Q2F0YTM='));
CALL sp_insert_song('Broken & Fixed', 'Repair', FROM_BASE64('UmVwYWly'));
CALL sp_insert_song('Loop-Repeat', 'Loopers', FROM_BASE64('UmVwZWF0'));
CALL sp_insert_song('Echoes Remix', 'Echoes', FROM_BASE64('UmVtaXg='));
CALL sp_insert_song('Echoes Remix 2', 'Echoes', FROM_BASE64('UmVtaXgy'));
CALL sp_insert_song('Parallel', 'Lines', FROM_BASE64('UGFyYWxsZWw='));
CALL sp_insert_song('Series I', 'Set', FROM_BASE64('U2VyaWVzMQ=='));
CALL sp_insert_song('Series II', 'Set', FROM_BASE64('U2VyaWVzMg=='));
CALL sp_insert_song('Series III', 'Set', FROM_BASE64('U2VyaWVzMw=='));
CALL sp_insert_song('Misc 1', 'Misc', FROM_BASE64('TWlzYzE='));
CALL sp_insert_song('Misc 2', 'Misc', FROM_BASE64('TWlzYzI='));
CALL sp_insert_song('Misc 3', 'Misc', FROM_BASE64('TWlzYzM='));
CALL sp_insert_song('Alt Take 1', 'Alt', FROM_BASE64('QWx0MQ=='));
CALL sp_insert_song('Alt Take 2', 'Alt', FROM_BASE64('QWx0Mg=='));
CALL sp_insert_song('Final Cut', 'EditTeam', FROM_BASE64('RmluYWw='));
CALL sp_insert_song('Rough Cut', 'EditTeam', FROM_BASE64('Um91Z2g='));
CALL sp_insert_song('Master', 'Mastering', FROM_BASE64('TWFzdGVy'));
CALL sp_insert_song('Pre-Master', 'Mastering', FROM_BASE64('UHJlTWVzdA=='));
CALL sp_insert_song('Outtake', 'Bloopers', FROM_BASE64('T3V0dGFrZQ=='));
CALL sp_insert_song('Bloop', 'Bloopers', FROM_BASE64('Qmxvb3A='));
CALL sp_insert_song('ShortBeep', 'Beeps', FROM_BASE64('QmVlcA=='));
CALL sp_insert_song('LongBeep', 'Beeps', FROM_BASE64('TG9uZ0JlZXA='));
CALL sp_insert_song('Test End', 'QA End', FROM_BASE64('VGVzdEVuZA=='));
CALL sp_insert_song('Overflow', 'EdgeCase', FROM_BASE64('T3ZlcmZsb3c='));
CALL sp_insert_song('Sparse Name', 'Sparse', FROM_BASE64('U3BhcnNl'));
CALL sp_insert_song('Dense Name With Many Words To Make A Very Wide Cell In The UI', 'Verbose One', FROM_BASE64('RGVuc2U='));
CALL sp_insert_song('Finale', 'ClosingAct', FROM_BASE64('RmluYWxl'));
CALL sp_insert_song('Curtain', 'ClosingAct', FROM_BASE64('Q3VydGFpbg=='));
CALL sp_insert_song('Encore', 'ClosingAct', FROM_BASE64('RW5jb3Jl'));
CALL sp_insert_song('Rewind', 'Player', FROM_BASE64('UmV3aW5k'));
CALL sp_insert_song('Forward', 'Player', FROM_BASE64('Rm9yd2FyZA=='));
CALL sp_insert_song('Skip', 'Player', FROM_BASE64('U2tpcA=='));
CALL sp_insert_song('Previous', 'Player', FROM_BASE64('UHJldg=='));
CALL sp_insert_song('Next', 'Player', FROM_BASE64('TmV4dA=='));
CALL sp_insert_song('Hidden Gem', 'Various', FROM_BASE64('SGVtbA=='));
CALL sp_insert_song('Treasure', 'Various', FROM_BASE64('VHJlYXN1cmU='));
CALL sp_insert_song('Weird___Name', 'Strange', FROM_BASE64('V2VpcmQ='));
CALL sp_insert_song('Odd/Name\\Test', 'Oddities', FROM_BASE64('T2Rk'));
CALL sp_insert_song('SpacesAnd-Tabs\tMixed', 'WeirdSpacing', FROM_BASE64('V2VpcmRTcGFjZQ=='));
CALL sp_insert_song('ControlChars\n\r', 'Controls', FROM_BASE64('Q29udHJvbA=='));
CALL sp_insert_song('NullChar\0Test', 'Nulls', FROM_BASE64('TnVsbA=='));
CALL sp_insert_song('TrailingDots...', 'Dots', FROM_BASE64('RG90cw=='));
CALL sp_insert_song('LeadingDots...', 'Dots', FROM_BASE64('RG90cw=='));
CALL sp_insert_song('CapsLock', 'KEYS', FROM_BASE64('S0VZUw=='));
CALL sp_insert_song('123-456-7890', 'Numbers', FROM_BASE64('MTIz'));
CALL sp_insert_song('Mix_123-AZ', 'Hybrid', FROM_BASE64('TXhJ'));
CALL sp_insert_song('Final Track', 'The End', FROM_BASE64('VGhlRW5k'));
CALL sp_insert_song('VeryFinalTrack', 'The End', FROM_BASE64('VmVyeUZpbmFs'));

INSERT INTO songs_backup (original_song_id, title, artist, mp3_data, backup_note, backed_up_by)
SELECT id, title, 'Broken Band', mp3_data, 'initial import', 'system' 
FROM songs_data WHERE id = 1;

INSERT INTO file_index (song_id, file_path, mp3_data, note) VALUES
(1, '/uploads/Test Song.mp3', NULL, 'copied to uploads and catalogued'),
(2, NULL, FROM_BASE64('U29tZUF1ZGlvX2luX2luZGV4'), 'audio stored directly in index');