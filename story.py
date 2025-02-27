story = """

In the village of Leawood, the land was soaked in quiet. Rolling hills surrounded the small town, and the only noises that punctuated the silence were the occasional rustle of wind through the trees or the chirp of a bird. But despite the peaceful scenery, a storm had been brewing. And in the heart of that village, a young woman named Isla stood by the window, staring at the darkened horizon.

It wasn’t the storm that caught her attention; it was something far more unsettling.

For weeks, there had been whispers about a strange phenomenon in the skies—a low rumble, distant yet constant, a sound that made the villagers uneasy. It wasn’t thunder, or at least not like any thunder they had ever heard. It was a deep, resonant echo, and every day it seemed to grow louder.

Isla had grown up with the storm sounds. They were familiar to her, comforting even. Her childhood was full of thunderstorm afternoons, curled up with her grandmother by the fire, listening to the rain. But this wasn’t the same. The echo wasn’t the natural rumble of a storm—it felt ancient, as though something far older than the village itself was awakening.

Her grandmother had been the one to first mention it. The older woman had spent countless hours telling Isla stories of the “Old Ones,” ancient spirits who once roamed the lands before the first settlers came to Leawood. They were legends to most, stories for children, but to Isla, they felt more like warnings.

Isla’s thoughts were interrupted as the door to the room creaked open. Her younger brother, Luca, stepped inside. His face was pale, eyes wide with fear.

“I heard it again,” he said in a whisper, as if speaking too loudly might make the sound grow louder.

Isla nodded, her expression serious. “I heard it too.”

Luca had always been the more sensitive of the two, prone to fear and uncertainty. Yet, there was something in his voice that told Isla this was different. He wasn’t just scared; he was terrified.

“It’s not just a storm,” Luca continued, his voice shaking. “It’s something... worse.”

Isla stood up from her place by the window and moved toward her brother. She took his hand in hers, offering him a small but reassuring smile.

“We’ll figure it out, Luca. We always do.”

But deep down, Isla wasn’t so sure. Something about the sound, that echo that seemed to grow louder each day, felt wrong. She couldn’t explain it, but it gnawed at her, as if something ancient and forgotten was clawing its way back to the surface.

That night, as the sky grew darker and the rumbling continued, Isla sat by the fire, her thoughts turning back to her grandmother’s stories. The Old Ones, those strange spirits from the past, were said to have lived in harmony with the land, drawing power from the earth itself. But that harmony had been broken when the first settlers arrived, pushing the spirits into hiding, where they had slumbered ever since.

But now, it seemed, they were stirring. And with them, the storm.

Isla couldn’t shake the feeling that the two were connected. That the rumble in the sky wasn’t just a natural occurrence—it was a signal. A sign that something was awakening.

The following morning, Isla set out to investigate. She wasn’t sure what she was looking for, but she knew she had to do something. She had spent her entire life in Leawood, and yet, there were still places in the surrounding woods she had never ventured—places her grandmother had warned her never to go. Today, she would have to confront those warnings.
As she walked deeper into the forest, the air grew heavier, the ground softer beneath her feet. The trees were dense, their branches twisting and turning in odd shapes, as if they had been bent by something far more powerful than the wind. The sound of the distant thunder echoed in the background, making the whole place feel alive, as though the forest itself was holding its breath.
After what felt like hours of walking, Isla reached a clearing. In the center stood an ancient stone circle, its stones covered in moss and vines. She had seen it before, in her grandmother’s stories, but she had never dared to approach it. Now, as she stood before it, she felt an undeniable pull. The stones seemed to hum with a strange energy, and the echo of thunder grew louder, as though it was emanating from the very ground beneath her feet.
Isla stepped closer to the circle, her heart pounding in her chest. She reached out to touch one of the stones, and the moment her fingers made contact, the ground trembled.
The thunder, which had been distant for so long, erupted around her. It was no longer a rumble but a roar, deafening and overwhelming. The sky above her crackled with energy, and the air became thick with the smell of ozone. Isla’s breath quickened as she pulled her hand back, but the force of the storm seemed to be drawing her in, pulling her toward the center of the circle.
Then, from the shadows of the trees, a figure emerged.
Isla’s heart skipped a beat. The figure was tall and cloaked in tattered robes, its face hidden beneath a hood. It moved with purpose, its steps silent despite the chaos around it. As it approached, Isla felt a chill run down her spine.
“Who are you?” she called out, her voice shaky.
The figure paused, and for a moment, Isla thought it might speak. But instead, it raised one hand and pointed to the center of the stone circle. Isla hesitated but then stepped forward, drawn by the undeniable force of the figure’s gesture.
As she entered the circle, the storm seemed to quiet, the rumble fading to a low murmur. The figure stepped into the circle as well, its presence now looming over her.
“You should not have come,” the figure’s voice was low, gravelly, and ancient. It sent shivers down Isla’s spine.
“Why?” Isla asked, her voice steady despite the fear threatening to rise within her.

The figure didn’t answer immediately. It seemed to be considering her words, its eyes hidden beneath the shadow of its hood.

“The Old Ones are awakening,” it finally said. “And with their return, the storm will come. The land will be changed forever.”

Isla’s mind raced. She had always known something was off, but now it felt as though everything she had ever been taught was about to be shattered.

“And what can we do?” she asked, her voice trembling.

The figure gave a slow, sorrowful shake of its head.

“Nothing. The storm has begun. The echoes are just the beginning.”

"""

def get_chunks():

    words = story.split()

    print("THE STORY HAS BEEN PRINTED.")
    length = len(words)
    chunks = [words[i:i+200] for i in range(0,length,200)]
    #for i in range(2):
    #    print(f"CHUNK{i}:")
    #    print(chunks[i])

    chunk_texts = [" ".join(chunk) for chunk in chunks]
    #for i in range(2):
    #    print(f"chunktext{i}:")
    #    print(chunk_texts[i])
    return chunk_texts