import os
from shutil import rmtree, copyfile

def inputValidation(smaller, larger, msg, isPlaylist):
    if isPlaylist == True:
        while(True):
            try:
                choice = int(input(msg))
            except ValueError:
                return "x"
            if choice >= smaller and choice <= larger: 
                return choice
            print("Invalid choice.")
    else: # not for playlists but to simply enter the index/numeration of the song
        while True:
            try:
                choice = input(msg)
                if choice == "x": return "x"
                elif int(choice) >= 0 and int(choice) <= larger and (len(choice) == 3): return choice
                print("Invalid choice. (accepted inputs: \"000\" to \"{}\")".format("{:03}".format(larger)))
            except ValueError:
                print("Invalid input.")

def getPlaylists():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return [f for f in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, f))]

def getSongs(specific_directory):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    specific_path = os.path.join(current_directory, specific_directory)
    files = [f for f in os.listdir(specific_path) if os.path.isfile(os.path.join(specific_path, f))]
    files.sort()
    return files

def displayPlaylists(playlists):
    print("\nAvailable playlists:")
    for playlist in enumerate(playlists):
        print("{}. {}".format(playlist[0]+1, playlist[1]))

def choosePlaylist(playlists, msg):
    displayPlaylists(playlists)
    choice = inputValidation(1, len(playlists), msg, True)
    if choice == "x": return "x"

    return playlists[choice-1]

def displaySongs(playlist):
    songs = getSongs(playlist)
    print("\nSongs from \"{}\":".format(playlist))
    for song in songs:
        print("{}".format(song))

def renameSong(playlists):
    print("Choose from the playlist the song you want to rename.")
    playlist = choosePlaylist(playlists, "\nEnter from which playlist: (enter \"x\" to cancel) ")
    if playlist == "x": return

    songs = getSongs(playlist)

    if len(songs) < 1:
        print("No songs in this playlist.")
        return
    
    displaySongs(playlist)
    choice = inputValidation(1, (len(songs) - 1), "\nEnter the numeric value of the song: (enter \"x\" to cancel) ", False)
    if choice == "x": return

    song = next(filter(lambda s: choice in s, songs), None)
    old = playlist + "/" + song
    old_index = song[:3]

    while(len(new := input("Enter new name (the numeration must not be typed): (press \"x\" to cancel) ")) < 1):
        print("Name of the song cannot be empty.")

    if new == "x": return
    new = playlist + "/" + old_index + ". " + new + ".mp3"
    os.rename(old, new)

def numenumerateSong(index, song, playlist):
    if index < 10:
        index = "00" + str(index)
        rename = str(index) + ". " + song
    elif index < 100:
        index = "0" + str(playlist)
        rename = str(index) + ". " + song
    os.rename(playlist + "/" + song, playlist + "/" + rename)
            
def checkifNumerated(playlist):
    songs = getSongs(playlist)
    numerated = True
    for index, song in enumerate(songs):
        if not (song[3] == "." and (int(song[2]) >= 0 and int(song[2]) <= 9)):
            numerated = False
            break

    if numerated == False:
        if input("Looks like some songs in \"{}\" are not numerated. Do you want to numerate them? (Y/n) ". format(playlist)) == "Y":
            for index, song in enumerate(songs):
                if not (song[3] == "." and (int(song[2]) >= 0 and int(song[2]) <= 9)):
                    numenumerateSong(index, song, playlist)
            return True
        else: return False
    
    return True

def closeGaps(playlist, songs):
    first_song = songs[0][5:]
    first_song_index = songs[0][:3]
    if int(first_song_index) != 0:
        os.rename((playlist + "/" + first_song_index + ". " + first_song), (playlist + "/000. " + first_song))
        songs[0] = "000. " + first_song

    for i, song in enumerate(songs):
        if i < (len(songs) - 1):
            current_index = song[:3]
            next_index = songs[i+1][:3]              
            next_song = songs[i+1][5:]
            diff = int(next_index) - int(current_index)
            if diff == 1: continue

            new_index = int(next_index) - (diff - 1)
            if new_index < 10: new_index = "00" + str(new_index) + ". "
            elif new_index < 100: new_index = "0" + str(new_index) + ". "

            songs[i+1] = new_index + next_song
            os.rename((playlist + "/" + next_index + ". " + next_song), (playlist + "/" + new_index + next_song))

def shifting(playlist, songs, song_index, position, moveUp):
    if moveUp == True:
        start = int(position)
        move = 1
        end = -1
    else:
        start = int(song_index)
        move = - 1
        end = int(position) + 1
    
    for song in songs[start:end]:
        next_strindex = song[:3]
        if next_strindex == song_index: continue
        next_intindex = int(next_strindex) + move
        if next_intindex < 10: new_strindex = "00" + str(next_intindex) + ". "
        elif next_intindex < 100: new_strindex = "0" + str(next_intindex) + ". "
        os.rename((playlist + "/" + song), (playlist + "/" + new_strindex + song[5:]))
    os.rename((playlist + "/" + songs[int(song_index)]), playlist + "/" + position + ". " + songs[int(song_index)][5:])

def sortPlaylist(playlists):
    songs = getSongs(playlist)
    if len(songs) >= 999:
        print("Playlist is full.")
        return

    playlist = choosePlaylist(playlists, "\nEnter which playlist you want to sort: (enter \"x\" to cancel) ")
    if playlist == "x": return
    
    while True:
        songs = getSongs(playlist)
        closeGaps(playlist, songs)
        displaySongs(playlist)

        song_index = inputValidation(0, (len(songs)-1), "\nEnter the numeric value of the song you want to sort: (enter \"x\" to cancel) ", False)
        if song_index == "x": return
        
        position = inputValidation(0, 999, "To what position should the song be moved? (enter \"x\" to cancel)            ", False)
        if position == "x": return
        if song_index == position: return

        shifting(playlist, songs, song_index, position, int(song_index) > int(position))

def moveSong(playlists): #to other playlist
    print("Choose from a playlist the song you want to move to another playlist.")
    src_playlist = choosePlaylist(playlists, "\nEnter from which playlist: (enter \"x\" to cancel) ")
    if src_playlist == "x": return

    songs = getSongs(src_playlist)

    if len(songs) < 1:
        print("No songs in this playlist.")
        return

    displaySongs(src_playlist)
    song_index = inputValidation(0, (len(songs)-1), "\nEnter the numeric value of the song you want to move: (enter \"x\" to cancel) ", False) 
    if song_index == "x": return

    song = next(filter(lambda s: song_index in s, songs), None)
    dst_playlist = choosePlaylist(playlists, "\nEnter the playlist you want to move the song to: (enter \"x\" to cancel) ")
    if dst_playlist == "x": return
    
    dst_playlist_songs = getSongs(dst_playlist)
    if len(dst_playlist_songs) >= 999:
        print("Song cannot be moved. Playlist is full.")
        return

    copyfile(src_playlist + "/" + song, dst_playlist + "/" + song)
    os.remove(src_playlist + "/" + song)
    print("Moved \"{}\" from \"{}\" to \"{}\".".format(song, src_playlist, dst_playlist))

    dst_playlist_songs = getSongs(dst_playlist)
    closeGaps(dst_playlist, dst_playlist_songs)
    songs = getSongs(src_playlist)
    closeGaps(src_playlist, songs)

def deleteSong(playlists):
    print("Choose from a playlist the song you want to delete.")
    playlist = choosePlaylist(playlists, "\nEnter from which playlist: (enter \"x\" to cancel) ")
    if playlist == "x": return

    songs = getSongs(playlist)

    if len(songs) < 1:
        print("No songs in this playlist.")
        return
    
    displaySongs(playlist)
    choice = inputValidation(1, len(songs), "\nChoose a song: (enter \"x\" to cancel) ", False) 
    if choice == "x": return

    song = next(filter(lambda s: choice in s, songs), None)

    Yn = input("Do you really want to permanently remove \"{}\" ? (Y/n): ".format(song)) 
    if Yn == "Y":
        os.remove(playlist + "/" + song)
        print("Removed: \"{}\" !".format(song))
    else:
        print("Canceled the deletion of \"{}\" .".format(song))

def deletePlaylist(playlists):
    print("Choose a playlist you want to delete.")
    playlist = choosePlaylist(playlists, "\nEnter which playlist you want to delete: (enter \"x\" to cancel) ")
    if playlist == "x": return

    Yn = input("Do you really want to permanently remove \"{}\" ? (Y/n): ".format(playlist))
    if Yn == "Y":
        rmtree(playlist)
        print("Removed: \"{}\" !".format(playlist))
    else:
        print("Canceled the deletion of \"{}\".".format(playlist))

def main():
    playlists = getPlaylists()

    if len(playlists) < 1:
        print("No playlists.")
        return
    
    for playlist in playlists:
        numerated = checkifNumerated(playlist)
    
    if numerated == False: 
        print("In order to use the playlist-manager the playlists need to be numerated.")
        return

    menu = "\n---------------------------------------------------------------\n|                      Choose an option:                      |\n---------------------------------------------------------------\n| 1. Display playlists             5. Rename song             |\n| 2. Display songs in playlist     6. Delete song             |\n| 3. Sort playlist                 7. Delete playlist         |\n| 4. Move song to other playlist   (Press \"x\" to exit.)       |\n---------------------------------------------------------------\nChoice: "
    while(True):
        try:
            choice = int(input(menu))
        except ValueError:
            return
        if choice == 1: displayPlaylists(playlists)
        elif choice == 2:
            playlist = choosePlaylist(playlists, "\nEnter from which playlist: (enter \"x\" to cancel) ")
            if playlist == "x": continue
            displaySongs(playlist)
        elif choice == 3: sortPlaylist(playlists)
        elif choice == 4: moveSong(playlists)
        elif choice == 5: renameSong(playlists)
        elif choice == 6: deleteSong(playlists)
        elif choice == 7: deletePlaylist(playlists)
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()