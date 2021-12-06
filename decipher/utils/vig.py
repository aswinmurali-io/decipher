import itertools
import re


def load_dictionary():
    with open('dictionary.txt') as file:
        englishWords = {
            word: None for word in file.read().split('\n')}
    return englishWords

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency


ENGLISH_LETTER_FREQUENCY = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07,
}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = LETTERS + LETTERS.lower() + ' \t\n'
NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 16
NONLETTERS_PATTERN = re.compile('[^A-Z]')
ENGLISH_WORDS = load_dictionary()


def get_english_count(message):
    message = remove_non_letters(message.upper())
    possible_words = message.split()

    if possible_words == []:
        return 0.0  # no words at all, so return 0.0

    matches = sum(word in ENGLISH_WORDS for word in possible_words)
    return float(matches) / len(possible_words)


def remove_non_letters(message):
    letters_only = [
        symbol for symbol in message if symbol in LETTERS_AND_SPACE]
    return ''.join(letters_only)


def is_english(message, word_percentage=20, letter_percentage=85):
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).
    words_match = get_english_count(message) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message))
    message_letters_percentage = float(num_letters) / len(message) * 100
    letters_match = message_letters_percentage >= letter_percentage
    return words_match and letters_match


def get_letter_count(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter.
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
                   'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def get_frequency_order(message):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    # first, get a dictionary of each letter and its frequency count
    msg_letter_freq = get_letter_count(message)

    # second, make a dictionary of each frequency count to each letter(s)
    # with that frequency
    freqToLetter = {}
    for letter in LETTERS:
        if msg_letter_freq[letter] not in freqToLetter:
            freqToLetter[msg_letter_freq[letter]] = [letter]
        else:
            freqToLetter[msg_letter_freq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string
    for freq, value in freqToLetter.items():
        value.sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple
    # pairs (key, value), then sort them
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=lambda x: x[0], reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all
    # the letters for the final string
    freqOrder = [freqPair[1] for freqPair in freqPairs]
    return ''.join(freqOrder)


def english_freq_match_score(message):
    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters is among the six most frequent and
    # six least frequent letters for English.
    freqOrder = get_frequency_order(message)

    matchScore = sum(commonLetter in freqOrder[:6]
                     for commonLetter in ETAOIN[:6])
    # Find how many matches for the six least common letters there are.
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore


def decrypt(key, message):
    translated = []  # stores the encrypted/decrypted message string

    keyIndex = 0
    key = key.upper()

    for symbol in message:  # loop through each character in message
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS
            num -= LETTERS.find(key[keyIndex])  # subtract if decrypting

            num %= len(LETTERS)  # handle the potential wrap-around

            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1  # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)

    return ''.join(translated)


def main():
    # ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    # ciphertext = """hl l ap vophoqh iq whlv wrud"""
    ciphertext = """
    Pv spd yqzr 1878 A pwbr ux ldgdde gb Lbjbnz nf Yddayqal we bge Gminazfpbx we Lamdgj, iak xqwbeqcev pw Albkmx ta fo ldzbbog bge onujom cymrkqindd xkz fbzfmnne hn ldm nyux. Pzvumg ukucsmsmc mk rtmzqrz bgmqe, U vak zcyf isbzctdd lk bul Nhnsh Znrldczimqtznp Euketvlzr ir Aerikpiaa Atzfeam. Tza zrnqlmmt izs kpigpwmmc iz Hnvei na bgm siyd, afz jrmwqm H catlv fwvu qs, bge edcgjl Nmogim wmq hsz jevsdv nuf. Nn dwvqpvf is Balbsu, Q yliqvdd fgal ig pvzoa gap zdnwvpll spqogfh ldm charmr, azc wso iyymzlx dqdp aj bul mmmly'e bomjbef. Q ewklavev, dwjlddz, vifg msjg bapdz nfrhcwna jow vmqe um tza antm rqsumsigj if tgrmkf, mmd kqkplmcmc iz qesypvuo Bimdmgaj ev fhndbx, wtdrw E nbbvc ux rqfieavg, hvc is ozbe wjbrymc cooz ly fae qbbhmr.

Ttd csixnpom jqogfhl dwavcqa znp orgiwgpwm bn mmmy, tqb svz lm ht tzd fkbupvf jtt yhsxkzgbvd imd phssobry. Q vir rqlonal sywl ux bdhgszm nul zbsaogev pw gom Amqkegijaa, jpbg egoy H swndrk is bge rztsh jnabkm nf Yziowvq. Apdzd I izs kpzhjs nv shq rhgqtqlz ag z Jqyaah jhstdb, vhubh kdigamqmc ttd bgjm nul fzzzqc tza ahikkiuimm ajpmef. Q rpnuxc hsrm shtkmm izso ldm uhvca nf fge eqzqlzncr Gtzzao pnk qs vnt ndef bwe apd ldvasigj iak kncqasd szkea ig Lcqrmx, mq kzqlzkg, vha shjae zl ibznse z psys-uvzrm, znp ruuymrkmc qm bdhnyevt tm rieexx tg ppr Izhbhst kifaa.

Jvzm ehtt oaaj, iak edij fdnm ldm cywkwmgqc hsnlfoqoa vhubh A diq bvcmqgame, A sif ymlwuep, vild i tymzb srmhn gb ebbvcmc sgefwnmez, bn bge nzsw dwfwqsik af Oekdijhz. Gmqe U qadhqrk, iml gap zljaiqf qlxqohdd kk nny ir bn bq zbda bb diks zbatt ldm jhzca, znp dvwj bb iirs z lustda ccvv spd vqqafziu, dpdv H wmr slncpr lnem bk dnlazvj ndddr, fgal ycezm nn nud Hnveia wwradsehofo. Nby unvshe ly denr dir ldsbzijal bm, iml vhqm al hifa Q bile fn mqomym iml aeozmw ywacikmrcqmt, A sif zw vmzk mmd wiippismc ttzt s imqpkzt aomqd vabryuhvdd fgal jwg h lzg rhatlv xm yvas qm sqmdajo zl jzkj ta Dnyhiak. Q vir durpspkull, zkbodcifctl, pv spd tdnohopvw Wqwmtqr, afz tnuldl z mamtz higlz nv Oodssekcgo rdbsy, ihtz ig ulikbg idqelnqrciatx rghnwz, jha ehbg pqqmaoavvv eznm m oalazaht fwuedmmwjb gv aommd fge fafg uqmm lozshk ev nabduotumg lk qzwzndd if.

H hsz vrpbgmq kush fkz xpv hv Dnskafz, iak eza shqqexkzr ha ezde mr aan—we ha ezde mr af evpvud we exdvwj auptkqmge znv oqkwmmkd a pzy oety wmquht m laf pw ol. Cmldr etcz yqejclasazbek, E vnacqiklk frsrqghbdl so Xnnvkv, gois oqems cwoacvwk qmta vhayp nst spd latnyazf hvc qclqqs gb bul Mlxhrq zrw ezelahasinky vnivumc. Bgedd I kpilll ewq sale leur hb z xqihztw dwglt hv shq Rtjwvq, smzlhns z cginbybkmrs, ydafevtsmra dxurtwjkr, hvc aoezcifc ahjp lwmek zs A diq, jwmahdqqathg zvzd nqeqky ldia P wtogt. En adwzzpvf lhd fge kpigl we ux fumafymf imbwle, fgal E abvv qmzluyev ppna Q lcrt qhtzaz ylium shq lelnwcvtha znp qukpqphbd anmqvhwnm vu bgm bogmtju, we apzb H mgrt ewsr h knuolqse shbryisqnn um mq oblsm nn kihhny. Ypbvahvf ttd lspbry ikbdrzztarm, V imfim bk lacevt bx lg lizc tg hmncm spd hased, wvq aw sije go mq mcnybdzr iz roea trza ozdtqmtakcf hvc tdse dxhavfpdd lnmubida.
    """
    hackedMessage = hack(ciphertext)

    if hackedMessage is not None:
        print(hackedMessage)


def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message.
    seqSpacings = {}  # keys are sequences, values are list of int spacings
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []  # initialize blank list

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1. For example, getUsefulFactors(144)
    # returns [2, 72, 3, 48, 4, 36, 6, 24, 8, 18, 9, 16, 12]

    if num < 2:
        return []  # numbers less than 2 have no useful factors

    factors = []  # the list of factors found

    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1):  # don't test 1
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))


def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors.
    factorCounts = {}  # key is a factor, value is how often if occurs

    # seqFactors keys are sequences, values are lists of factors of the
    # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them.
    factorsByCount = [
        (factor, value)
        for factor, value in factorCounts.items()
        if factor <= MAX_KEY_LENGTH
    ]

    # Sort the list by the factor count.
    factorsByCount.sort(key=lambda x: x[1], reverse=True)

    return factorsByCount


def kasiski_examination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the ciphertext. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # See getMostCommonFactors() for a description of seqFactors.
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # See getMostCommonFactors() for a description of factorsByCount.
    factorsByCount = getMostCommonFactors(seqFactors)

    return [twoIntTuple[0] for twoIntTuple in factorsByCount]


def getNthSubkeysLetters(n, keyLength, message):
    # Returns every Nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('', message.upper())

    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def hack_with_key_lengths(ciphertext, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key.
    ciphertextUp = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(
            nth, mostLikelyKeyLength, ciphertextUp)

        # freqScores is a list of tuples like:
        # [(<letter>, <Eng. Freq. match score>), ... ]
        # List is sorted by match score. Higher score means better match.
        # See the englishFreqMatchScore() comments in freqAnalysis.py.
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = decrypt(
                possibleKey, nthLetters)
            keyAndFreqMatchTuple = (
                possibleKey, english_freq_match_score(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        # Sort by match score
        freqScores.sort(key=lambda x: x[1], reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    # Try every combination of the most likely letters for each position
    # in the key.
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Create a possible key from the letters in allFreqScores
        possibleKey = ''.join(
            allFreqScores[i][indexes[i]][0] for i in range(mostLikelyKeyLength)
        )

        decryptedText = decrypt(
            possibleKey, ciphertextUp)

        if is_english(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            return decryptedText

    # No English-looking decryption found, so return None.
    return None


def hack(ciphertext):
    key_lengths = kasiski_examination(ciphertext)

    processed_msg = None

    for keyLength in key_lengths:
        processed_msg = hack_with_key_lengths(ciphertext, keyLength)
        if processed_msg is not None:
            break

    if processed_msg is None:
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            if keyLength not in key_lengths:
                processed_msg = hack_with_key_lengths(ciphertext, keyLength)
                if processed_msg is not None:
                    break

    return processed_msg


if __name__ == '__main__':
    main()
