import json
import re

gages_text = """
PHASE 1 – Échauffement & Connexion (Hot 1-2)
1.	Homme : Embrasse langoureusement la Femme pendant 60 secondes en tenant son visage entre tes mains. Tags: #baiser #sensuel #slow #softcore Hot: 1
2.	Femme : Assieds-toi sur les genoux de l’Homme face à lui et fais-lui un massage des épaules et du cou pendant 90 secondes. Tags: #massage #caresses #softcore Hot: 1
3.	Homme : Caresse les cuisses et les fesses de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 1
4.	Femme : Réalise un strip-tease lent et enlève seulement un vêtement. Tags: #striptease #déshabillage #softcore Hot: 1
5.	Homme : Masse les seins de la Femme par-dessus son soutien-gorge pendant 90 secondes. Tags: #seins #caresses #softcore Hot: 2
6.	Femme : Embrasse et lèche le torse et les tétons de l’Homme pendant 75 secondes. Tags: #oral #teasing #softcore Hot: 2
7.	Homme : Bande les yeux de la Femme et caresse tout son corps avec la plume pendant 2 minutes. Tags: #plume #bandeau #teasing #softcore Hot: 2
8.	Femme : Fais une fellation douce à l’Homme par-dessus son caleçon pendant 90 secondes. Tags: #oral #fellation #softcore Hot: 2
9.	Homme : Bois une bière entière lentement. Tags: #alcool Hot: 1
10.	Femme : Lèche le cou et les oreilles de l’Homme pendant 60 secondes. Tags: #baiser #teasing #softcore Hot: 1
11.	Homme : Massage les pieds de la Femme pendant 2 minutes. Tags: #massage #softcore Hot: 1
12.	Femme : Fais un lapdance habillée sur l’Homme pendant 90 secondes. Tags: #lapdance #grinding #softcore Hot: 2
13.	Homme : Caresse le ventre et l’intérieur des cuisses de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 1
14.	Femme : Embrasse l’Homme avec un french kiss profond pendant 75 secondes. Tags: #baiser #softcore Hot: 1
15.	Homme : Utilise le masse-tête sur le dos et les fesses de la Femme pendant 2 minutes. Tags: #massage #softcore Hot: 1
16.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 1
17.	Homme : Embrasse le ventre de la Femme en descendant lentement pendant 60 secondes. Tags: #baiser #teasing #softcore Hot: 2
18.	Femme : Caresse le sexe de l’Homme par-dessus son pantalon pendant 75 secondes. Tags: #teasing #caresses #softcore Hot: 2
19.	Homme : Bande les yeux de la Femme et caresse son visage et son cou pendant 90 secondes. Tags: #bandeau #sensuel #softcore Hot: 1
20.	Femme : Assieds-toi dos contre l’Homme et frotte-toi doucement contre lui pendant 90 secondes. Tags: #grinding #teasing #softcore Hot: 2
21.	Homme : Caresse les cheveux et le dos de la Femme pendant 2 minutes. Tags: #caresses #sensuel #softcore Hot: 1
22.	Femme : Embrasse le torse de l’Homme tout en caressant ses bras pendant 75 secondes. Tags: #baiser #caresses #softcore Hot: 2
23.	Homme : Bois une gorgée de gin ou de cocktail. Tags: #alcool Hot: 1
24.	Femme : Danse sensuellement contre le corps de l’Homme pendant 90 secondes. Tags: #striptease #teasing #softcore Hot: 2
25.	Homme : Caresse les seins de la Femme par-dessus ses vêtements pendant 75 secondes. Tags: #seins #caresses #softcore Hot: 2
26.	Femme : Lèche lentement les lèvres et le cou de l’Homme. Tags: #baiser #softcore Hot: 1
27.	Homme : Massage les cuisses de la Femme pendant 2 minutes. Tags: #massage #teasing #softcore Hot: 1
28.	Femme : Frotte ta poitrine contre le torse de l’Homme pendant 90 secondes. Tags: #grinding #teasing #softcore Hot: 2
29.	Homme : Bande les yeux de la Femme et caresse ses bras et jambes avec la plume. Tags: #bandeau #plume #softcore Hot: 1
30.	Femme : Fais un massage de la tête et des tempes de l’Homme pendant 90 secondes. Tags: #massage #softcore Hot: 1
31.	Homme : Caresse les fesses de la Femme par-dessus ses vêtements pendant 90 secondes. Tags: #teasing #caresses #softcore Hot: 2
32.	Femme : Embrasse et mordille doucement les oreilles de l’Homme. Tags: #baiser #softcore Hot: 2
33.	Homme : Bois la moitié d’une bière. Tags: #alcool Hot: 1
34.	Femme : Caresse le torse de l’Homme avec tes ongles doucement pendant 75 secondes. Tags: #caresses #teasing #softcore Hot: 2
35.	Homme : Embrasse les mains et les poignets de la Femme. Tags: #baiser #softcore Hot: 1
36.	Femme : Assieds-toi sur les genoux de l’Homme et frotte-toi légèrement contre lui. Tags: #grinding #softcore Hot: 2
37.	Homme : Massage les épaules de la Femme avec de l’huile. Tags: #massage #huile #softcore Hot: 1
38.	Femme : Réalise un strip-tease lent d’un seul accessoire. Tags: #striptease #softcore Hot: 1
39.	Homme : Caresse le dos de la Femme sous ses vêtements. Tags: #caresses #softcore Hot: 2
40.	Femme : Embrasse l’Homme avec un french kiss tout en caressant sa nuque. Tags: #baiser #softcore Hot: 2

PHASE 2 – Déshabillage & Sensualité Peau à Peau (Hot 2-3)
1.	Homme : Enlève le haut de la Femme et masse ses seins nus pendant 2 minutes. Tags: #seins #caresses #déshabillage #softcore Hot: 2
2.	Femme : Fais une fellation lente et nue à l’Homme pendant 2 minutes. Tags: #oral #fellation #softcore Hot: 3
3.	Homme : Caresse le clitoris de la Femme avec tes doigts par-dessus sa culotte pendant 2 minutes. Tags: #doigts #clito #teasing #masturbation #softcore Hot: 3
4.	Femme : Réalise un strip-tease complet jusqu’à rester en lingerie. Tags: #striptease #déshabillage #softcore Hot: 2
5.	Homme : Lèche les tétons de la Femme pendant 90 secondes. Tags: #oral #seins #softcore Hot: 3
6.	Femme : Fais un massage érotique du dos et des fesses de l’Homme avec de l’huile. Tags: #massage #huile #softcore Hot: 2
7.	Homme : Insère les boules de geisha à la Femme et fais-la marcher pendant 90 secondes. Tags: #jouet #teasing #softcore Hot: 3
8.	Femme : Lèche les testicules et le périnée de l’Homme pendant 2 minutes. Tags: #oral #softcore Hot: 3
9.	Homme : Bois les deux tiers d’une bière. Tags: #alcool Hot: 2
10.	Femme : Chevauche l’Homme nue avec seulement un frottement extérieur pendant 3 minutes. Tags: #grinding #teasing #softcore Hot: 3
11.	Homme : Caresse tout le corps nu de la Femme avec la plume pendant 3 minutes. Tags: #plume #teasing #softcore Hot: 2
12.	Femme : Faites un 69 léger avec seulement des baisers et caresses pendant 2 minutes. Tags: #69 #oral #softcore Hot: 3
13.	Homme : Stimule le clitoris de la Femme avec tes doigts pendant 3 minutes. Tags: #doigts #clito #masturbation #softcore Hot: 3
14.	Femme : Lèche les tétons de l’Homme tout en le branlant doucement. Tags: #oral #doigts #masturbation #softcore Hot: 3
15.	Homme : Enlève la culotte de la Femme avec tes dents. Tags: #striptease #teasing #softcore Hot: 2
16.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 2
17.	Homme : Massage le périnée de l’Homme pendant 2 minutes. Tags: #teasing #softcore Hot: 3
18.	Femme : Fais un titjob avec tes seins sur le sexe de l’Homme pendant 2 minutes. Tags: #titjob #teasing #softcore Hot: 3
19.	Homme : Bande les yeux de la Femme, utilise la plume et tes doigts sur son corps. Tags: #bandeau #plume #doigts #softcore Hot: 3
20.	Femme : Fais un lapdance complètement nue sur l’Homme pendant 3 minutes. Tags: #lapdance #grinding #softcore Hot: 3
21.	Homme : Caresse tout le corps nu de la Femme pendant 3 minutes. Tags: #caresses #sensuel #softcore Hot: 2
22.	Femme : Fais une fellation à l’Homme les yeux bandés pendant 2 minutes. Tags: #oral #fellation #bandeau #softcore Hot: 3
23.	Homme : Stimule les seins et les tétons de la Femme pendant 3 minutes. Tags: #seins #caresses #softcore Hot: 3
24.	Femme : Caresse le sexe de l’Homme avec du lubrifiant pendant 2 minutes. Tags: #lubrifiant #doigts #masturbation #softcore Hot: 3
25.	Homme : Bois un shot de gin ou de cocktail. Tags: #alcool Hot: 2
26.	Femme : Frotte ton clitoris contre la cuisse de l’Homme. Tags: #grinding #masturbation #teasing #softcore Hot: 3
27.	Homme : Lèche le ventre et les hanches de la Femme. Tags: #oral #teasing #softcore Hot: 2
28.	Femme : Massage les testicules de l’Homme pendant 2 minutes. Tags: #caresses #softcore Hot: 3
29.	Homme : Bande les yeux de la Femme et caresse l’intérieur de ses cuisses. Tags: #bandeau #teasing #softcore Hot: 3
30.	Femme : Chevauche l’Homme en lingerie pendant 3 minutes. Tags: #grinding #softcore Hot: 3
31.	Homme : Caresse les fesses nues de la Femme. Tags: #caresses #softcore Hot: 3
32.	Femme : Lèche le périnée et les testicules de l’Homme. Tags: #oral #softcore Hot: 3
33.	Homme : Caresse l’anus externe de la Femme pendant 2 minutes. Tags: #anal #prep #softcore Hot: 3
34.	Femme : Branle l’Homme lentement pendant 2 minutes. Tags: #doigts #masturbation #softcore Hot: 3
35.	Homme : Fais un massage complet du corps de la Femme avec de l’huile. Tags: #massage #huile #softcore Hot: 2
36.	Femme : Embrasse l’Homme profondément tout en caressant son sexe. Tags: #baiser #teasing #softcore Hot: 3
37.	Homme : Stimule le clitoris de la Femme avec la plume. Tags: #plume #clito #masturbation #softcore Hot: 3
38.	Femme : Retiens ton excitation pendant 1 minute (edging). Tags: #edging #rétention #softcore Hot: 3
39.	Homme : Caresse doucement l’anus de la Femme. Tags: #anal #prep #softcore Hot: 3
40.	Femme : Fais un lapdance accompagné de baisers profonds. Tags: #lapdance #baiser #softcore Hot: 3

PHASE 3 – Excitation Orale & Jouets (Hot 3-4)
1.	Homme : Fais un cunnilingus à la Femme pendant 4 minutes. Tags: #oral #cunnilingus #softcore Hot: 4
2.	Femme : Fais une fellation profonde à l’Homme pendant 4 minutes. Tags: #oral #fellation #softcore Hot: 4
3.	Homme : Utilise le rabbit vibrator sur le clitoris de la Femme pendant 4 minutes. Tags: #jouet #vibration #clito #masturbation #softcore Hot: 4
4.	Femme : Suce l’Homme tout en portant les boules de geisha. Tags: #oral #jouet #softcore Hot: 4
5.	Homme : Combine doigts et cunnilingus pendant 4 minutes. Tags: #doigts #oral #softcore Hot: 4
6.	Femme : Fais un deepthroat pendant 3 minutes. Tags: #oral #fellation #softcore Hot: 4
7.	Homme : Insère lentement le plug anal à la Femme avec beaucoup de lubrifiant pendant 3 minutes. Tags: #anal #plug #lubrifiant #prep #softcore Hot: 4
8.	Femme : Branle l’Homme tout en léchant partout pendant 4 minutes. Tags: #doigts #oral #masturbation #softcore Hot: 4
9.	Homme : Bois un shot de cocktail. Tags: #alcool Hot: 3
10.	Femme : Faites un 69 complet pendant 5 minutes. Tags: #69 #oral #softcore Hot: 4
11.	Homme : Utilise le rabbit tout en léchant les seins de la Femme. Tags: #jouet #oral #softcore Hot: 4
12.	Femme : Fais une fellation avec les boules de geisha en toi. Tags: #oral #jouet #softcore Hot: 4
13.	Homme : Insère doucement un doigt anal avec lubrifiant pendant 4 minutes. Tags: #anal #prep #lubrifiant #softcore Hot: 4
14.	Femme : Lèche tout le corps de l’Homme en descendant lentement. Tags: #oral #softcore Hot: 4
15.	Homme : Contrôle le rabbit sur la Femme pendant 5 minutes. Tags: #jouet #teasing #softcore Hot: 4
16.	Femme : Fais une fellation intense pendant 4 minutes. Tags: #oral #fellation #softcore Hot: 4
17.	Homme : Combine plug anal et stimulation du clito. Tags: #anal #jouet #softcore Hot: 4
18.	Femme : Bois un cocktail entier. Tags: #alcool Hot: 3
19.	Homme : Combine cunnilingus et rabbit. Tags: #oral #jouet #softcore Hot: 4
20.	Femme : Fais une fellation tout en massant le périnée. Tags: #oral #teasing #softcore Hot: 4
21.	Homme : Stimule le vagin et le clito avec tes doigts pendant 4 minutes. Tags: #doigts #masturbation #softcore Hot: 4
22.	Femme : Suce l’Homme en chevauchant son visage. Tags: #69 #oral #softcore Hot: 4
23.	Homme : Fais de l’edging à la Femme pendant 3 minutes. Tags: #edging #rétention #masturbation #softcore Hot: 4
24.	Femme : Fais un titjob intense pendant 3 minutes. Tags: #titjob #softcore Hot: 4
25.	Homme : Utilise le plug anal avec vibrations. Tags: #anal #jouet #softcore Hot: 4
26.	Femme : Fais un deepthroat en regardant l’Homme dans les yeux. Tags: #oral #softcore Hot: 4
27.	Homme : Fais un cunnilingus intense. Tags: #oral #softcore Hot: 4
28.	Femme : Alterne branlette rapide et lente (edging). Tags: #doigts #masturbation #edging #softcore Hot: 4
29.	Homme : Applique du lubrifiant et caresse analement. Tags: #anal #lubrifiant #softcore Hot: 4
30.	Femme : Faites un 69 avec le rabbit. Tags: #69 #jouet #softcore Hot: 4
31.	Homme : Contrôle le rythme de la fellation de la Femme. Tags: #oral #teasing #softcore Hot: 4
32.	Femme : Retiens ton orgasme pendant 2 minutes (edging). Tags: #edging #rétention #softcore Hot: 4
33.	Homme : Utilise plusieurs jouets en même temps. Tags: #jouet #softcore Hot: 4
34.	Femme : Fais une fellation en caressant les testicules. Tags: #oral #softcore Hot: 4
35.	Homme : Combine doigts et plug anal. Tags: #doigts #anal #softcore Hot: 4
36.	Femme : Lèche tout le corps de l’Homme très lentement. Tags: #oral #slow #softcore Hot: 4
37.	Homme : Contrôle totalement le rabbit sur la Femme. Tags: #jouet #teasing #softcore Hot: 4
38.	Femme : Fais un oral tout en faisant de l’edging à l’Homme. Tags: #oral #edging #softcore Hot: 4
39.	Homme : Fais une préparation anale avancée. Tags: #anal #prep #softcore Hot: 4
40.	Femme : Fais une fellation tout en caressant tes seins. Tags: #oral #seins #softcore Hot: 4

PHASE 4 – Intensité & Préparation Anale (Hot 4-5)
1.	Homme : Pénètre vaginalement la Femme lentement pendant 6 minutes. Tags: #pénétration #sexe #slow #softcore Hot: 4
2.	Femme : Chevauche l’Homme en gardant le contrôle total pendant 6 minutes. Tags: #sexe #cowgirl #softcore Hot: 5
3.	Homme : Alterne pénétration vaginale et plug anal. Tags: #pénétration #anal #softcore Hot: 5
4.	Femme : Laisse l’Homme te prendre en missionnaire profonde pendant 6 minutes. Tags: #pénétration #missionnaire #softcore Hot: 5
5.	Homme : Combine cunnilingus, doigts et plug anal. Tags: #oral #anal #softcore Hot: 4
6.	Femme : Fais une fellation très intense pendant 5 minutes. Tags: #oral #softcore Hot: 4
7.	Homme : Prends la Femme en levrette pendant 6 minutes. Tags: #pénétration #levrette #softcore Hot: 5
8.	Femme : Utilise le rabbit sur toi pendant que tu suces l’Homme. Tags: #jouet #oral #softcore Hot: 4
9.	Homme : Tente une pénétration anale très lente et préparée. Tags: #anal #softcore Hot: 5
10.	Femme : Bois un grand verre de cocktail. Tags: #alcool Hot: 4
11.	Homme : Baise la Femme fermement sans douleur. Tags: #sexe #intense #hardcore #softcore Hot: 5
12.	Femme : Chevauche l’Homme avec le plug anal. Tags: #sexe #anal #softcore Hot: 5
13.	Homme : Faites un 69 très intense. Tags: #69 #oral #softcore Hot: 4
14.	Femme : Prends la position amazone pendant 6 minutes. Tags: #sexe #softcore Hot: 5
15.	Homme : Utilise tous les jouets en même temps sur la Femme. Tags: #jouet #softcore Hot: 4
16.	Femme : Fais une fellation et avale si tu le désires. Tags: #oral #softcore Hot: 5
17.	Homme : Combine pénétration et stimulation anale. Tags: #pénétration #anal #softcore Hot: 5
18.	Femme : Laisse l’Homme te prendre comme il veut pendant 7 minutes. Tags: #sexe #intense #hardcore #softcore Hot: 5
19.	Homme : Porte le plug anal pendant que tu pénètres la Femme. Tags: #anal #sexe #softcore Hot: 5
20.	Femme : Fais de l’edging à l’Homme pendant 4 minutes. Tags: #edging #rétention #softcore Hot: 5
21.	Homme : Prends la Femme en position cuillères profondes. Tags: #pénétration #softcore Hot: 5
22.	Femme : Contrôle ton propre orgasme (edging). Tags: #edging #rétention #masturbation #softcore Hot: 5
23.	Homme : Prends la Femme en levrette avec le rabbit. Tags: #pénétration #jouet #softcore Hot: 5
24.	Femme : Chevauche l’Homme de façon intense. Tags: #sexe #hardcore #softcore Hot: 5
25.	Homme : Combine anal play et pénétration vaginale. Tags: #anal #pénétration #softcore Hot: 5
26.	Femme : Continue la fellation jusqu’au bout. Tags: #oral #softcore Hot: 5
27.	Homme : Missionnaire avec les jambes de la Femme sur tes épaules. Tags: #pénétration #softcore Hot: 5
28.	Femme : Retiens ton plaisir pendant 3 minutes. Tags: #edging #rétention #softcore Hot: 5
29.	Homme : Pénètre la Femme debout. Tags: #sexe #softcore Hot: 5
30.	Femme : Utilise les jouets sur l’Homme. Tags: #jouet #softcore Hot: 4
31.	Homme : Réalise une pénétration anale complète très lente si accepté. Tags: #anal #softcore Hot: 5
32.	Femme : Sexe oral mutuel très intense. Tags: #69 #oral #softcore Hot: 5
33.	Homme : Pénètre avec beaucoup de lubrifiant. Tags: #pénétration #lubrifiant #softcore Hot: 5
34.	Femme : Laisse-toi complètement aller. Tags: #sexe #intense #hardcore #softcore Hot: 5
35.	Homme : Contrôle l’orgasme de la Femme. Tags: #edging #softcore Hot: 5
36.	Femme : Chevauche l’Homme tout en l’embrassant. Tags: #sexe #cowgirl #softcore Hot: 5
37.	Homme : Prends la Femme en levrette avec un léger hairpulling consensuel. Tags: #pénétration #hairpulling #softcore Hot: 5
38.	Femme : Combine plusieurs jouets et oral. Tags: #jouet #oral #softcore Hot: 5
39.	Homme : Pénètre lentement avec beaucoup de teasing. Tags: #pénétration #teasing #softcore Hot: 5
40.	Femme : Prends le contrôle total pendant 7 minutes. Tags: #sexe #softcore Hot: 5

PHASE 5 – Sexe Libre & Climax (Hot 5)
1.	Homme : Baise la Femme dans ta position préférée pendant 8 à 10 minutes. Tags: #pénétration #sexe #hardcore #softcore Hot: 5
2.	Femme : Chevauche l’Homme jusqu’à ce qu’il jouisse. Tags: #sexe #cowgirl #softcore Hot: 5
3.	Homme : Prends la Femme en levrette profonde pendant 8 minutes. Tags: #pénétration #levrette #hardcore #softcore Hot: 5
4.	Femme : Fais une fellation et avale. Tags: #oral #softcore Hot: 5
5.	Homme : Pénètre la Femme tout en utilisant le plug anal sur elle. Tags: #pénétration #anal #softcore Hot: 5
6.	Femme : Laisse l’Homme te prendre de façon intense et consentie. Tags: #sexe #intense #hardcore #softcore Hot: 5
7.	Homme : Faites un sexe oral mutuel très intense. Tags: #69 #oral #softcore Hot: 5
8.	Femme : Atteins plusieurs orgasmes avec le rabbit et l’Homme. Tags: #jouet #masturbation #softcore Hot: 5
9.	Homme : Réalise une pénétration anale complète si accepté. Tags: #anal #softcore Hot: 5
10.	Femme : Bois un dernier verre puis baise l’Homme comme tu veux. Tags: #alcool #sexe #softcore Hot: 5
11.	Homme : Prends la Femme en missionnaire avec les jambes relevées. Tags: #pénétration #missionnaire #softcore Hot: 5
12.	Femme : Masturbe l’Homme jusqu’à l’orgasme avec ta bouche et tes mains. Tags: #masturbation #oral #softcore Hot: 5
13.	Homme : Baise la Femme debout contre un mur. Tags: #sexe #hardcore #softcore Hot: 5
14.	Femme : Chevauche l’Homme en amazone intense. Tags: #sexe #softcore Hot: 5
15.	Homme : Combine pénétration et stimulation du clito avec le rabbit. Tags: #pénétration #jouet #softcore Hot: 5
16.	Femme : Laisse l’Homme te prendre en cuillères tout en te caressant. Tags: #sexe #softcore Hot: 5
17.	Homme : Fais de l’edging à la Femme avant de la pénétrer. Tags: #edging #pénétration #softcore Hot: 5
18.	Femme : Masturbe-toi devant l’Homme puis laisse-le te prendre. Tags: #masturbation #teasing #softcore Hot: 5
19.	Homme : Prends la Femme en levrette avec léger hairpulling. Tags: #pénétration #hairpulling #hardcore #softcore Hot: 5
20.	Femme : Contrôle le rythme et fais jouir l’Homme comme tu veux. Tags: #sexe #softcore Hot: 5
21.	Homme : Pénètre la Femme tout en utilisant le plug anal et le rabbit. Tags: #pénétration #anal #jouet #softcore Hot: 5
22.	Femme : Fais une fellation très profonde jusqu’à la fin. Tags: #oral #softcore Hot: 5
23.	Homme : Baise la Femme en missionnaire en la regardant dans les yeux. Tags: #pénétration #missionnaire #softcore Hot: 5
24.	Femme : Retiens ton orgasme le plus longtemps possible puis lâche-toi. Tags: #edging #rétention #softcore Hot: 5
25.	Homme : Prends la Femme par derrière avec beaucoup de lubrifiant. Tags: #pénétration #lubrifiant #softcore Hot: 5
26.	Femme : Utilise tous les jouets sur toi pendant que l’Homme te regarde. Tags: #jouet #masturbation #softcore Hot: 5
27.	Homme : Alterne pénétration vaginale et anal play. Tags: #pénétration #anal #softcore Hot: 5
28.	Femme : Chevauche l’Homme jusqu’à ce que vous jouissiez ensemble. Tags: #sexe #cowgirl #softcore Hot: 5
29.	Homme : Baise la Femme de façon intense et passionnée. Tags: #sexe #hardcore #softcore Hot: 5
30.	Femme : Masturbe l’Homme avec tes seins et ta bouche. Tags: #titjob #oral #masturbation #softcore Hot: 5
31.	Homme : Prends la Femme en position debout ou contre un meuble. Tags: #sexe #softcore Hot: 5
32.	Femme : Laisse l’Homme te doigter et te lécher jusqu’à l’orgasme. Tags: #doigts #oral #softcore Hot: 5
33.	Homme : Pénètre lentement puis accélère progressivement. Tags: #pénétration #teasing #softcore Hot: 5
34.	Femme : Prends le contrôle total et baise l’Homme comme tu le désires. Tags: #sexe #softcore Hot: 5
35.	Homme : Combine tous les jouets et la pénétration. Tags: #jouet #pénétration #softcore Hot: 5
36.	Femme : Fais un 69 intense jusqu’à l’orgasme mutuel. Tags: #69 #oral #softcore Hot: 5
37.	Homme : Baise la Femme en cuillères tout en stimulant son clito. Tags: #pénétration #clito #softcore Hot: 5
38.	Femme : Masturbe-toi sur le sexe de l’Homme avant la pénétration. Tags: #masturbation #teasing #softcore Hot: 5
39.	Homme : Prends la Femme comme tu veux pour le final. Tags: #sexe #hardcore #softcore Hot: 5
40.	Femme : Laisse-toi aller complètement et jouis plusieurs fois. Tags: #sexe #softcore Hot: 5
"""

def parse_gages(text):
    gages = []
    current_phase = 0
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Phase header
        phase_match = re.match(r'PHASE (\d+)', line)
        if phase_match:
            current_phase = int(phase_match.group(1))
            continue
            
        # Gage line
        gage_match = re.match(r'(\d+)\.\s+(Homme|Femme)\s*:\s*(.*?)Tags:\s*(.*?)\s+Hot:\s*(\d+)', line)
        if gage_match:
            id_in_phase = int(gage_match.group(1))
            target = gage_match.group(2)
            description = gage_match.group(3).strip()
            tags_str = gage_match.group(4).strip()
            hot = int(gage_match.group(5))
            
            # Robust tag extraction
            tags = []
            # Split by space or comma, then clean
            for part in re.split(r'[ ,]+', tags_str):
                clean_tag = part.replace('#', '').strip()
                if clean_tag:
                    tags.append(clean_tag)
            
            # Duration extraction
            duration = 0
            sec_match = re.search(r'pendant (\d+)\s*secondes?', description, re.IGNORECASE)
            if sec_match:
                duration = int(sec_match.group(1))
            else:
                min_match = re.search(r'pendant (\d+)\s*minutes?', description, re.IGNORECASE)
                if min_match:
                    duration = int(min_match.group(1)) * 60
                else:
                    range_match = re.search(r'pendant (\d+)\s*à\s*(\d+)\s*minutes?', description, re.IGNORECASE)
                    if range_match:
                        duration = int(range_match.group(1)) * 60
            
            gages.append({
                "id": len(gages) + 1,
                "phase": current_phase,
                "target": target,
                "text": description,
                "tags": tags,
                "hot": hot,
                "duration": duration
            })
            
    return gages

all_gages = parse_gages(gages_text)
with open('data/gages.json', 'w', encoding='utf-8') as f:
    json.dump(all_gages, f, ensure_ascii=False, indent=2)

print(f"Parsed {len(all_gages)} gages.")
