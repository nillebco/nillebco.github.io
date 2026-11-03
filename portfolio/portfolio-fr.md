# 🎯 Portfolio

## Parler avec une page web

Tags: #extension-web #chrome #safari #desktop #iOS

Trop long à lire ? Laissez la page web vous parler. Demandez un résumé, posez des questions, exécutez des fonctions simples. Disponible sur toutes les pages, inclut un mode Lecteur (pour afficher ce que l'assistant en temps réel lit)

Fonctionne bien avec [Serveur de clés éphémères OpenAI](#serveur-de-clés-éphémères-openai)

[vidéo promotionnelle](https://youtube.com/shorts/YD_as_008lI)
[code source](https://github.com/nillebco/web-extension-voice-rt)
[changelog](https://github.com/nillebco/web-extension-voice-rt/blob/main/CHANGELOG.md)

## Serveur de clés éphémères OpenAI

Tags: #service #openai

Service simple basé sur nodeJS qui renvoie des clés éphémères OpenAI pour la vidéo en temps réel (validité : 1 minute)

## Assistant personnel pour Signal, Telegram, WhatsApp

Tags: #gemini #mistral #claude #openai #whatsapp #signal #telegram #social-interactions #ai

Pendant longtemps, j'ai hébergé un proxy vers OpenAI via Signal, WhatsApp et Telegram. Je pensais que l'accès à l'IA devrait être partagé avec des amis, car c'est incroyablement utile dans les interactions sociales (faire un résumé des conversations en cours, accéder à des outils, effectuer des tâches simples, accéder à différents modèles selon les besoins, ...)

### En savoir plus

[Un Assistant de Messagerie Instantanée basé sur l'IA](https://nilleb.co/blog/#un-assistant-de-messagerie-instantanée-basé-sur-lia)

## Gestion des ressources Azure, GCP, Hetzner avec terraform

Tags: #devops #terraform #gcp #azure #hetzner

L'Infrastructure as Code permet la reproductibilité, la traçabilité et l'observabilité aux organisations. Chaque organisation est unique, avec ses propres politiques. Nous utilisons terraform pour gérer les ressources organisationnelles dans des environnements Cloud Native, et les politiques sentinel pour appliquer les exigences organisationnelles.

Mots-clés : points de terminaison privés, zones DNS privées, groupes de sécurité réseau, équilibreurs de charge, profils frontdoor, fonctions et applications conteneurisées, serveurs de base de données (cosmosdb, postgres, sql server, mongodb), applications azuread et octrois d'administrateur de domaine. Pare-feu Hetzner, sous-réseaux et hôtes. Google Cloud Storage, instances cloud run, fonctions.

## Services d'échange de jetons

Dans le web d'aujourd'hui, nous avons plusieurs identités. Presque une pour chaque site.

Les services d'échange de jetons permettent une intégration transparente entre différentes applications web — typiquement une digital workplace qui dialogue avec des plateformes de gamification, de recherche, d'analytics et de reconnaissance des collaborateurs, sans que l'utilisateur ait à se reconnecter.

## Un chatbot répondant à toute question liée à LumApps

Tags: #LLM #Q&A #RAG #retrieval-augmented-generation #formats-conversion

[LumApps](https://www.lumapps.com/) (un Digital Workplace) propose un [site web de documentation public](https://docs.lumapps.com/docs/). C'est une mine d'or, et un terrain de jeu idéal pour la génération augmentée par la récupération.

Nous avons donc :

- extrait tout son contenu (vous pouvez utiliser la boîte à outils lumapps OU utiliser l'un de nos crawlers)
- converti en markdown
- divisé en chunks (choisir la bonne taille est primordial)
- nettoyé (vous savez, ce "Demander une modification de cette documentation." et quelques autres)
- converti les chunks en embeddings (multiqampnet, pour être honnête - c'est moins cher qu'OpenAI et fait un excellent travail)
- stocké tous les chunks dans une base de données vectorielle - nous aimons Rust, donc qdrant était un match parfait.

C'est tout pour la partie stockage d'information

Chaque fois qu'un utilisateur pose une question à notre bot, nous :

- convertissons la question en embeddings,
- calculons les éléments les plus proches dans qdrant,
- sélectionnons les 100 résultats les plus élevés.
- préparons un prompt (c'est le jargon des développeurs pour "formater la question de manière à forcer OpenAI à répondre sans inventer la réponse et mettre en évidence les sources")
  - (le prompt inclut comme contexte certains des résultats précédemment sélectionnés)
- envoyons tout cela à notre IA générative préférée

Nous affichons à l'écran la réponse d'OpenAI.

---

Voici un échantillon de ce que nous obtenons, en interrogeant notre petit LumDocsBot :

> **Q: Quels widgets sont supportés sur mobile ?**
>
> Les widgets supportés sur mobile incluent Commentaires, Liste de contenu, Drive, Image mise en avant, Liste de fichiers, Gestion de fichiers, Contenu HTML, iFrame, Galerie d'images, Introduction, Liens, Lecture obligatoire, Métadonnées, Lecture, Titre, Liste d'utilisateurs et Vidéo. [Source](https://docs.lumapps.com/docs/mobile-l3073093865382487)
>
> **Q: Que dois-je faire pour construire un assistant digital ?**
>
> Pour créer un nouvel assistant digital, vous devez aller dans l'application web Assistant Digital et vous connecter, cliquer sur NOUVEL assistant pour ouvrir l'assistant de personnalisation, sélectionner une langue standard (en ou fr), créer l'assistant, lui donner une personnalité, ajouter des adresses e-mail pour les utilisateurs que vous souhaitez ajouter en tant que Personnel technique et Gestionnaires d'assistant, et configurer les connaissances de l'assistant en construisant des ressources et en améliorant la compréhension. Source : https://docs.lumapps.com/docs/knowledge-l9660062419741646DA
>
> **Q: Mes intégrations Google ne fonctionnent pas. Pouvez-vous m'aider ?**
>
> Vérifiez quels droits sont accordés pour l'application LumApps côté administrateur Google. Allez sur https://admin.google.com/ac/apps/gmail/marketplace/domaininstall. Assurez-vous que l'application LumApps est activée pour toutes les UO contenant les utilisateurs qui devraient accéder aux intégrations GSuite. Si elle n'est pas activée, suivez la documentation Google (https://support.google.com/a/answer/172931?hl=fr) pour l'activer. Dans l'application LumApps, accédez à Accès aux données et assurez-vous que tous les services Google dont vous avez besoin sont Accordés. Si le Statut indique Partiellement accordé ou Révoqué, cela signifie que certains services ne sont pas accessibles par LumApps. Assurez-vous de leur accorder l'accès. Si les intégrations n'apparaissent toujours pas dans LumApps, désinstallez l'application LumApps dans GSuite et essayez de l'installer à nouveau. Assurez-vous de ne pas sauter d'étape de la documentation d'installation LumApps (https://docs.lumapps.
>
> **Quelles sont les dimensions personnalisées dans Google Analytics 4** ?
>
> ID Client, Nom du Client, ID du Site, Nom du Site, Slug du Site, Type Interne du Contenu, ID du Type de Contenu, Nom du Type de Contenu, Le Contenu est-il une Page d'accueil, ID du Contenu, Titre du Contenu, Slug du Contenu, IDs des Tags du Contenu, Tags du Contenu, IDs des Métadonnées du Contenu, Métadonnées du Contenu, Termes de Recherche, L'Utilisateur est-il Admin, Langue Principale de l'Utilisateur, et Langue Secondaire de l'Utilisateur. Source : https://docs.lumapps.com/docs/knowledge-l24187961517950485
