import random 
from datetime import datetime
random.seed(datetime.now().timestamp())

prompts = {
    "Mystical Forest Cat": "A majestic feline with emerald-green eyes sits regally on a moss-covered log in an enchanted, moonlit forest. Towering ancient trees with twisted branches are draped in glowing, ethereal vines. Soft mist swirls around the cat's paws as bioluminescent mushrooms illuminate the forest floor. The air is thick with magic, and faint celestial light pierces through the dense canopy.", 

    "Futuristic Dog Cityscape": "A robotic dog stands confidently on a bustling city street in a cyberpunk metropolis, with neon-lit skyscrapers stretching into the sky. The dog's metallic fur gleams under the lights, and its glowing eyes scan the surroundings. Hovering cars and holographic billboards fill the sky, while rain softly falls, reflecting the vibrant colors of the city. People in sleek futuristic outfits pass by, their faces illuminated by the city's vibrant glow.", 

    "Elegant Renaissance Garden with a Peacock": "An opulent Renaissance-style garden, filled with marble statues, meticulously manicured hedges, and vibrant flower beds. A magnificent peacock with iridescent feathers struts proudly near a stone fountain, which glistens in the golden afternoon sunlight. The garden is framed by towering cypress trees, with classical columns and a grand palace visible in the distance. The scene is serene, a perfect blend of natural beauty and architectural grandeur.", 

    "Whimsical Floating Islands with Birds": "A fantastical scene of floating islands suspended high above the clouds, connected by delicate rope bridges. Each island is lush with tropical foliage, vibrant flowers, and crystal-clear waterfalls cascading into the sky. Exotic, brightly colored birds soar between the islands, leaving shimmering trails of light in their wake. The sky is painted in hues of orange, pink, and purple as the sun sets on this otherworldly paradise.", 

    "Steampunk Cat in a Clockwork City": "A sleek, brass-plated cat prowls the cobblestone streets of a steampunk-inspired city, where towering clockwork buildings and steam-powered airships dominate the skyline. The cat's mechanical tail ticks like a clock, and its eyes glow with an electric blue light. Gears and cogs turn in the background as steam billows from chimneys. The air smells of oil and metal, with a faint hum of machinery all around.", 

    "Celestial Wolf in the Northern Lights": "A lone wolf with shimmering silver fur stands on the snowy peak of a mountain, howling toward the sky as the aurora borealis dances above. The wolf's eyes glow with an ethereal light, mirroring the vibrant greens, purples, and blues of the northern lights. Below, the snow-covered forest reflects the mystical glow from the heavens, and the stars seem unusually bright, twinkling like diamonds in the crisp, cold air.", 

    "Medieval Dragon Battle at Dusk": "A fierce dragon with ruby-red scales swoops down from the darkening sky, its massive wings creating gusts of wind over a medieval battleground. Knights in shining armor raise their shields, swords glinting in the fading sunlight. The dragon's fiery breath ignites the twilight, casting long shadows across the rugged, rocky landscape. The scene is filled with tension as the last rays of sun disappear, leaving the world bathed in an ominous glow.", 

    "Ethereal Underwater Castle": "A grand underwater palace built from iridescent coral and shimmering pearl stands in the depths of a vast, tranquil ocean. Schools of brightly colored fish dart through its arches, and graceful jellyfish with bioluminescent tendrils float lazily by. Kelp forests sway gently in the current, and sunlight filters down from the surface, casting long, wavy beams across the castle's domes and spires. The scene is serene, yet brimming with ancient, mystical energy.", 

    "Gothic Vampire Masquerade": "A grand ballroom illuminated by flickering candlelight, where guests in lavish, dark velvet attire swirl through a masquerade. The vampires, with pale skin and glowing red eyes, wear ornate, gilded masks, their capes sweeping dramatically as they move to hauntingly beautiful music. Stained-glass windows cast eerie, multicolored shadows across the polished marble floor, while long, flowing curtains sway in the breeze from the open gothic arches.", 

    "Surreal Desert Landscape with Giant Sculptures": "An endless desert of golden sands, where gigantic, otherworldly statues emerge from the dunes, towering over the horizon. The sky is an unusual shade of deep purple, with twin suns setting in the distance. Each sculpture is ancient and worn, yet detailed with intricate carvings, depicting forgotten gods and mythical creatures. The wind carries the whispers of the past, and the atmosphere is both serene and mysterious.", 

    "Majestic Phoenix Rising from Ashes": "A glorious phoenix, ablaze with vibrant hues of gold, crimson, and orange, emerges from a pile of smoldering ashes in a desolate landscape. Its wings spread wide, casting a radiant glow across the barren ground, while embers and fiery sparks swirl in the air around it. The sky above is painted in dramatic shades of red and purple as the sun sets, illuminating the bird's powerful resurgence.", 

    "Victorian Steampunk Airship Adventure": "A colossal brass-and-copper airship floats above the clouds, its hull adorned with ornate gears, pipes, and sails that gleam in the sunlight. On the deck, dapper passengers in Victorian-era attire peer through brass spyglasses, their long coats billowing in the wind. Below, a sprawling city of domed buildings and smoke-filled factories can be seen, while other airships and flying contraptions soar in the distance, each powered by steam and intricate clockwork mechanisms.", 

    "Enchanted Library of Floating Books": "A vast, dimly lit library with towering bookshelves that stretch endlessly into the darkness. Suspended in midair are hundreds of glowing books, their pages turning as if by an unseen force. The room is filled with a soft, magical glow, with shafts of light filtering through stained-glass windows depicting mythical creatures. The atmosphere is serene and mystical, with a sense of ancient wisdom swirling in the air, and an ornate wooden desk sits at the center, inviting curious minds to explore.", 

    "Dreamlike Floating Whale Above a City": "A massive, translucent whale swims gracefully through the sky above a peaceful, modern city at dawn. Its body glows faintly, casting soft blue and silver light over the buildings below. Wisps of clouds swirl around the whale as it moves, and its gentle song reverberates through the air, creating an otherworldly yet serene atmosphere. The city beneath wakes to this mystical sight, bathed in the soft golden light of the rising sun.", 

    "Samurai Duel in a Cherry Blossom Grove": "Two samurai stand poised for combat in the middle of a serene cherry blossom grove, their hands resting on the hilts of their katana. The ground is covered in a delicate blanket of pink petals, and more fall gracefully from the trees above. The air is still, with only the soft rustling of leaves and the distant sound of a bamboo water fountain. Sunlight filters through the branches, casting a dappled glow over the tense, silent scene, as both warriors prepare for the swift, decisive moment.", 

    "Alien Jungle with Luminescent Flora": "A dense, alien jungle where colossal trees with twisted, bioluminescent trunks tower overhead. The ground is alive with glowing, otherworldly plants, their tendrils reaching toward the sky. Strange, floating orbs of light drift through the air, illuminating paths between thick vines and massive, fern-like growths. In the distance, the silhouette of a mysterious creature with glowing eyes moves silently through the vegetation, leaving behind a shimmering trail of light.", 

    "Elegant Art Deco Ballroom with Jazz Band": "An opulent Art Deco ballroom adorned with sleek geometric patterns, shining gold accents, and towering black-and-white marble pillars. A lively jazz band plays on a grand stage, their music filling the air as elegantly dressed couples sway across the polished floor. Above, crystal chandeliers sparkle in the light, casting intricate reflections across the room. The scene is filled with glamour, energy, and the spirit of a golden age.", 

    "Galactic Landscape with a Space Station": "A sprawling space station orbits a distant, ringed planet, surrounded by nebulae and shimmering stars. The station's sleek, silver domes reflect the cosmic beauty around it, while small spacecraft zip between its structures. Below, the planet's rings cast soft shadows on its surface, which is dotted with swirling clouds and vast oceans. The vastness of space creates a sense of wonder and isolation, as the station floats peacefully in the silence of the cosmos.", 

    "Ancient Temple in a Hidden Jungle": "A moss-covered stone temple, half-buried by the encroaching jungle, stands in silence beneath a dense canopy of ancient trees. Vines snake their way up the temple's crumbling walls, and the sound of distant waterfalls echoes through the humid air. Shafts of sunlight pierce through the dense foliage, casting golden light on intricately carved statues of forgotten deities. The air is thick with the scent of damp earth and the mystery of long-lost civilizations.", 

    "!!!Futuristic Neon Samurai in a Cyberpunk City": "A lone samurai stands on the rain-slicked streets of a neon-drenched cyberpunk city, their glowing katana humming with energy. Towering skyscrapers covered in neon signs and holographic advertisements loom overhead, and the streets are alive with the bustle of futuristic cars and shadowy figures in trench coats. The samurai's sleek, high-tech armor reflects the vibrant colors of the city, and rain drips from the brim of their hat as they prepare for a silent, high-stakes showdown."
}


def random_pickup():
    prompt_keys = list(prompts.keys())

    random__prompt_key = prompt_keys[ random.randrange( 0, len(prompt_keys) ) ]

    random_prompt = prompts[random__prompt_key]

    return random_prompt

def generate_pos_neg_prompt():
    neg = "blurry, low resolution, pixelated, distorted, deformed, extra limbs, missing parts, unnatural anatomy, overexposed, underexposed, harsh lighting, cartoonish, 3D render, plastic, oversaturated, dull, watermark, text, logo, extra eyes, warped, unnatural textures, crowded background, out of focus, motion blur, grainy, noisy, low detail."
    pos = random_pickup()
    print(pos)
    return pos, neg

if __name__ == '__main__':
    print(generate_prompt_from_format())