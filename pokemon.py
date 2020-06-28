class Trainer:

    def __init__(self, name, team, num_potions, current_pokemon):
        self.name = name #string with the trainer's name
        self.team = team #list with the trainers pokemon
        self.num_potions = num_potions #integer with the number of potions the trainer has
        self.current_pokemon = current_pokemon #integer that is the index of the current pokemon from the team list
    
    def __repr__(self):
        
        return self.name + " has " + str(len(self.team)) + " pokemon and " + str(self.num_potions) + " potions.\nHis current pokemon is " + str(self.team[self.current_pokemon])
    
    #Method to add pokemon the the team
    def add_pokemon(self, pokemon):
        
        if len(self.team) < 6:
            self.team.append(pokemon)
            print("You caught a(n) " + pokemon.name + '.')
        else: #Trainer's team already has 6 pokemon
            print("Your team is already full! You'll need to release a pokemon if you want to catch " + pokemon)
    
    def use_potion(self):
        
        #This method heals the currently active pokemon
        pokemon = self.team[self.current_pokemon]

        #Only heal conscious pokemon
        if pokemon.is_knocked_out:
            print("Potions cannot revive KOed pokemon. Use a revive instead.")
        
        #Need potions to heal
        elif self.num_potions == 0:
            print("You're out of potions!")

        #Don't heal if the pokemon is at full health
        elif pokemon.current_hp == pokemon.max_hp:
            print("{name} is already at full health. Save the potion for when you need it!".format(name=pokemon.name))
            
        else:
            print("You use a potion to heal {pokemon}.".format(pokemon=pokemon.name))
            pokemon.heal(20)
            self.num_potions -= 1 #Remove the used potion
            print("You have {number} potions left.".format(number=self.num_potions))

class Pokemon:

    def __init__(self, name, level, type, max_hp, current_hp, is_knocked_out):
        self.name = name                        #string with the name of the pokemon
        self.level = level                      #integer with the pokemon's level
        self.type = type                        #string with the pokemon's type
        self.max_hp = max_hp                    #integer with the pokemon's max health
        self.current_hp = current_hp            #integer with the pokemon's current health
        self.is_knocked_out = is_knocked_out    #boolean describing whether the pokemon is knocked out
    
    def __repr__(self):
        return self.name + ": lvl "+ str(self.level) + ", " + self.type + " type, " + str(self.current_hp) + "/" + str(self.max_hp) + " HP"

    def take_damage(self, damage):
        
        #Deal the damage to the Pokemon and print out the damage done
        self.current_hp -= damage
        print("{name} takes {damage} points of damage.".format(name=self.name, damage=damage))
        
        if self.current_hp > 0: #Pokemon still has HP
            print("{name} now has {hp}/{max} HP.".format(name=self.name, hp=self.current_hp, max=self.max_hp))
        else: #Pokemon has dropped to 0 HP
            self.is_knocked_out = True
            self.current_hp = 0
            print("{name} has been knocked out!".format(name=self.name))
    
    def heal(self, health):
        
        #Check that the pokemon can be healed
        if not self.is_knocked_out and self.current_hp < self.max_hp:
            self.current_hp += health
            
            if self.current_hp > self.max_hp: #Can't heal above max HP
                self.current_hp = self.max_hp
           
            print("{name} healed and now has {hp}/{max} HP!".format(name=self.name,hp=self.current_hp,max=self.max_hp))
        
        #Can't heal if they are already at max HP
        elif self.current_hp == self.max_hp:
           print("{name} doesn't need to heal, they are already at max HP!".format(name=self.name))
        
        #Can't heal a Pokemon who is knocked out
        else: 
            print("{name} is knocked out! You'll need to revive them before they can heal.".format(name=self.name))

    def revive(self, health):
        
        if self.is_knocked_out:
            self.current_hp = health
            print("{name} is no longer knocked out and is back to {health} HP!".format(name=self.name, health=health))
        
        else: #
            print("{name} isn't knocked out! Save the revive for someone who needs it.".format(name=self.name))
            
    def attack(self, other_pokemon):

       #Certain types have advantage/disadvantage when attacking other types
       #Source: https://pokemondb.net/type - Gen 6+ Type table
        advantage = {
            "Normal": [],
            "Fire": ["Grass", "Ice", "Bug", "Steel"], 
            "Water": ["Fire", "Ground", "Rock"],
            "Electric": ["Water", "Flying", ], 
            "Grass": ["Water", "Ground", "Rock"],
            "Ice": ["Grass", "Ground", "Flying", "Dragon"],
            "Fighting": ["Normal", "Ice", "Rock", "Dark", "Steel"],
            "Poison": ["Grass", "Fairy"],
            "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
            "Flying": ["Grass", "Fighting", "Bug"],
            "Psychic": ["Fighting", "Poison", ],
            "Bug": ["Grass", "Psychic", "Dark"],
            "Rock": ["Fire", "Ice", "Flying", "Bug"],
            "Ghost": ["Psychic", "Ghost"],
            "Dragon": ["Dragon"],
            "Dark": ["Psychic", "Ghost"],
            "Steel": ["Ice", "Rock", "Fairy"],
            "Fairy": ["Fighting", "Dragon", "Dark"]
            }
        
        disadvantage = {
            "Normal": ["Rock", "Steel"],
            "Fire": ["Fire", "Water", "Rock", "Dragon"], 
            "Water": ["Water", "Grass", "Dragon", ],
            "Electric": ["Electric", "Grass", "Dragon"], 
            "Grass": ["Fire", "Grass", "Poison", "Flying", "Bug", "Dragon"],
            "Ice": ["Fire", "Water", "Ice", "Steel"],
            "Fighting": ["Poison", "Flying", "Psychic", "Bug", "Fairy"],
            "Poison": ["Poison", "Ground", "Rock", "Ghost"],
            "Ground": ["Grass", "Bug"],
            "Flying": ["Electric", "Rock", "Steel"],
            "Psychic": ["Psychic", "Steel"],
            "Bug": ["Fire", "Fighting", "Poison", "Flying","Ghost", "Steel", "Fairy"],
            "Rock": ["Fighting", "Ground", "Steel"],
            "Ghost": ["Dark"],
            "Dragon": ["Steel"],
            "Dark": ["Fighting", "Dark", "Fairy"],
            "Steel": ["Fire", "Water", "Electric", "Steel"],
            "Fairy": ["Fire", "Fighting", "Dark"]
            }
        
        immune = {
            "Normal": ["Ghost"],
            "Electric": ["Ground"],
            "Fighting": ["Ghost"],
            "Poison": ["Steel"],
            "Ground": ["Flying"],
            "Psychic": ["Dark"],
            "Ghost": ["Normal"],
            "Dragon": ["Fairy"]
        }
            
        print("{we} attacks {them}!".format(we=self.name,them=other_pokemon.name))
        
        #Attacking pokemon has a type advantage
        if other_pokemon.type in advantage[self.type]:
            print("It's super effective!")
            other_pokemon.take_damage(2*self.level)

        #Attacking pokemon has a type disadvantage    
        elif other_pokemon.type in disadvantage[self.type]:
            print("It's not very effective.")
            other_pokemon.take_damage(self.level//2)
        
        #The target's type is immune to the attacking pokemon's type
        elif other_pokemon.type in immune[self.type]:
            print("{attacking}'s attack has no effect on {target}!".format(attacking=self.name, target=other_pokemon.name))
        
        #Attacking pokemon has no type advantage/disadvantage
        else:
            other_pokemon.take_damage(self.level)


#Initialize pokemon here
bayleef = Pokemon("Bayleef", 16, "Grass", 57, 57, False)
crocanaw = Pokemon("Crocanaw", 12, "Water", 62, 62, False)
quilava = Pokemon("Quilava", 14, "Fire", 60, 60, False)
miltank = Pokemon("Miltank", 15, "Normal", 79, 79, False)
gastly = Pokemon("Gastly", 9, "Ghost", 50, 50 , False)
pikachu = Pokemon("Pikachu", 12, "Electric", 43, 43, False)
sandshrew = Pokemon("Sandshrew", 12, "Ground", 44, 44, False)

#Add trainers here
ash = Trainer("Ash", [bayleef, crocanaw, quilava, miltank, gastly], 5, 0)

#Test functionality here
ash.use_potion()