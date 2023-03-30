def printf_clear():
  with open('log.txt', 'w') as f:
    f.write('Hi')


def printf(*text):
  with open('log.txt', 'a', newline=None) as f:
    for t in text:
      f.write(str(t))
    f.write("\n")


class Boite:

  def __init__(self, _L=1, _l=1, _h=1):
    self.L = _L
    self.l = _l
    self.h = _h

  def set_dim(self):
    # printf("Veuillez entrer les valeurs suivantes :")
    self.L = int(input("longueur : "))
    self.l = int(input("largeur : "))
    self.h = int(input("hauteur : "))

  def get_dim(self):
    return [self.L, self.l, self.h]


class Carton(Boite):

  def __init__(self, _L=1, _l=1, _h=1):
    Boite.__init__(self, _L, _l, _h)
    self.contenu = []
    self.nb_boites = 0

  def add_boites(self, rotation, nb_L, nb_l, nb_h):
    self.contenu.append([rotation, nb_L, nb_l, nb_h])
    self.nb_boites += nb_L * nb_l * nb_h

  def remove_boites(self, rotation, nb_L, nb_l, nb_h):
    self.contenu.remove([rotation, nb_L, nb_l, nb_h])
    self.nb_boites -= nb_L * nb_l * nb_h

  def __gt__(self, other):
    if self.nb_boites > other.nb_boites:
      return True
    else:
      return False

  def copy(self):
    new_carton = Carton(self.L, self.l, self.h)
    new_carton.contenu = self.contenu[:]
    new_carton.nb_boites = self.nb_boites

    return new_carton

  def __str__(self):
    return "printf Carton :\ndimensions : " + str(self.L) + "x" + str(self.l) + "x" + str(self.h) + "\nnb_boites : " + str(self.nb_boites) + "\ncontenu : " + str(self.contenu)

  def combine(self, other):
    # printf("COMBINE !!", str(self), str(other))
    self.nb_boites += other.nb_boites
    self.contenu += other.contenu
    # printf(self)
    # printf("DONE !!")

  def print_placement(self):
    text_to_print=""
    num_etape = 1
    text_to_print+=f"Placement des boites dans le carton :\n{num_etape}. Positionnez le carton avec le long coté vers soi.\n"
    print(f"Placement des boites dans le carton :\n{num_etape}. Positionnez le carton avec le long coté vers soi.")
    for step in self.contenu:
      num_etape+=1
      rotation_text=""
      if step[0]==1:
          rotation_text="à plat avec le long côté de la boite dans le même sens que le long côté du carton"
      elif step[0]==2:
          rotation_text="sur la longue tranche avec le long côté de la boite dans le même sens que le long côté du carton"
      elif step[0]==3:
          rotation_text="à plat avec le long côté de la boite dans le même sens que le court côté du carton"
      elif step[0]==4:
          rotation_text="sur la petite tranche avec le long côté de la boite dans le même sens que le long côté du carton"
      elif step[0]==5:
          rotation_text="sur la longue tranche avec le long côté de la boite dans le même sens que le petit côté du carton"
      elif step[0]==6:
          rotation_text="sur la petite tranche avec le long côté de la boite dans le même sens que le petit côté du carton"
      
      print(f"{num_etape}. Positionnez (L*l*h) {step[1]}*{step[2]}*{step[3]} = {step[1]*step[2]*step[3]} carton(s) " + rotation_text)
      text_to_print+=f"{num_etape}. Positionnez (L*l*h) {step[1]}*{step[2]}*{step[3]} = {step[1]*step[2]*step[3]} carton(s) " + rotation_text + "\n"
    print(f"Vous avez maintenant placé {self.nb_boites} boite(s) dans le carton")
    text_to_print+=f"Vous avez maintenant placé {self.nb_boites} boite(s) dans le carton\n"

    return text_to_print

def possibilites(l):
  # renvoie lensemble des arrangements possibles de la liste (3d)
  p = []

  for i in range(3):
    k = [0, 1, 2]
    n1 = k[i]

    k.remove(n1)
    for j in range(2):
      n2 = k[j % 2]
      n3 = k[(j + 1) % 2]
      a = [l[n1], l[n2], l[n3]]
      printf(a)
      p.append(a)

  return p

"""
[180, 139, 65]
[180, 65, 139]
[139, 180, 65]
[139, 65, 180]
[65, 180, 139]
[65, 139, 180]
"""

def fill_carton(liste_carton,
                presentoire,
                fill_reste=True,
                _carton_precedent=Carton()):
  best_carton = Carton()
               
  
  for carton in liste_carton:
    # nb_cartons_total = nb_cartons_precedent
    # nb_cartons = 0
    n = 0  # pour savoir le nombre d'itération de dim
    for dim in possibilites(presentoire.get_dim()):
      cartons_reste = []
      carton_precedent = _carton_precedent.copy()   
      # if (fill_reste): printf("\n" * 2 + "-+*+-" * 10 + "________base")
      # else: printf("________reste")
      # printf(dim, " in ", carton.get_dim())

      n += 1
      # printf("n=", n)

      nb_L = carton.L // dim[0]
      L = dim[0] * nb_L
      L_r = carton.L - L
      # printf(f"{L_r=}")

      nb_l = carton.l // dim[1]
      l = dim[1] * nb_l
      l_r = carton.l - l
      # printf(f"{l_r=}")

      nb_h = carton.h // dim[2]
      h = dim[2] * nb_h
      h_r = carton.h - h
      # printf(f"{h_r=}")

      # actual_state.append([n, ["L", nb_L], ["l", nb_l], ["h", nb_h]])
      carton.add_boites(n, nb_L, nb_l, nb_h)

      carton_precedent.combine(carton)

      # printf(f"{nb_h}")
      # nb_cartons = nb_L * nb_l * nb_h
      # if (fill_reste):
      # nb_cartons_total += nb_cartons
      # printf("nb cartons=", nb_L, "x", nb_l, "x", nb_h, " =", nb_cartons)
      # printf("nb cartons_du carton=", nb_L, "x", nb_l, "x", nb_h, " =", carton.nb_boites)
      # printf("total=", carton_precedent.nb_boites)
      # printf("total=", carton_precedent.contenu)
      # printf("total=", L, "x", l, "x", h)
      # printf("reste=", L_r, "x", l_r, "x", h_r)

       # CHECK IF IT IS THE BEST CARTON
      if carton_precedent > best_carton:
        best_carton = carton_precedent.copy()

      # Fill the gaps
      if (fill_reste):
        carton_L = Carton(L_r, carton.l, carton.h)
        carton_l = Carton(carton.L, l_r, carton.h)
        carton_h = Carton(carton.L, carton.l, h_r)
        cartons_reste.append(carton_L)
        cartons_reste.append(carton_l)
        cartons_reste.append(carton_h)
        # printf("="*10 + "\nAFFICHAGE DES CARTONS FILLS \n" + "="*10)
        # for c in cartons_reste:
        #   printf(c)

        best_carton_fill = fill_carton(cartons_reste, presentoire, False, carton_precedent.copy())

        if best_carton_fill > best_carton:
          best_carton = best_carton_fill.copy()

      carton.remove_boites(n, nb_L, nb_l, nb_h)

  # printf("\n\n\n")
  # printf("*" * 20)
  # # printf("nb_cartons=", nb_cartons_total)
  # printf("best carton=", best_carton.nb_boites)
  # printf("contenu=", best_carton.contenu)
  # printf("*" * 20)
  return best_carton.copy()

#***********************************************************************************


import tkinter as tk

def validate_sizes(instruction_filling_box_text):
    
    global big_box_width
    global big_box_height
    global big_box_depth
    global small_box_width
    global small_box_height
    global small_box_depth
    
    big_box_width = big_box_width_entry.get()
    big_box_height = big_box_height_entry.get()
    big_box_depth = big_box_depth_entry.get()
    small_box_width = small_box_width_entry.get()
    small_box_height = small_box_height_entry.get()
    small_box_depth = small_box_depth_entry.get()

    if not big_box_width.isdigit() or not big_box_height.isdigit() or not big_box_depth.isdigit() or not small_box_width.isdigit() or not small_box_height.isdigit() or not small_box_depth.isdigit():
        validation_label.config(text="Please enter positive integers for all box dimensions.")
        return False

    big_box_size = f"{big_box_width} x {big_box_height} x {big_box_depth}"
    small_box_size = f"{small_box_width} x {small_box_height} x {small_box_depth}"

    carton = Carton(int(big_box_width), int(big_box_height), int(big_box_depth))
    presentoire = Boite(int(small_box_width), int(small_box_height), int(small_box_depth))
    best_carton = fill_carton([carton], presentoire)

    global root
    root.title("Result")
    root.geometry("1000x500")
    result_label.config(text=f"Big box size: {big_box_size}\nSmall box size: {small_box_size}\n\n" + str(best_carton.print_placement()))
    validation_label.config(text="")
    return True

def on_confirm(instruction_filling_box_text):
    if validate_sizes(instruction_filling_box_text):
        # do something with the box sizes here
        print("Box sizes confirmed")

def ui(instruction_filling_box_text):
  global root
  root = tk.Tk()
  root.title("Box Size Input")
  root.geometry("400x350")

  global big_box_label
  big_box_label = tk.Label(root, text="Big Box Size")
  big_box_label.pack()

  global big_box_width_label
  big_box_width_label = tk.Label(root, text="Width:")
  big_box_width_label.pack()

  global big_box_width_entry
  big_box_width_entry = tk.Entry(root)
  big_box_width_entry.pack()

  global big_box_height_label
  big_box_height_label = tk.Label(root, text="Height:")
  big_box_height_label.pack()

  global big_box_height_entry
  big_box_height_entry = tk.Entry(root)
  big_box_height_entry.pack()

  global big_box_depth_label
  big_box_depth_label = tk.Label(root, text="Depth:")
  big_box_depth_label.pack()

  global big_box_depth_entry
  big_box_depth_entry = tk.Entry(root)
  big_box_depth_entry.pack()

  global small_box_label
  small_box_label = tk.Label(root, text="Small Box Size")
  small_box_label.pack()

  global small_box_width_label
  small_box_width_label = tk.Label(root, text="Width:")
  small_box_width_label.pack()

  global small_box_width_entry
  small_box_width_entry = tk.Entry(root)
  small_box_width_entry.pack()

  global small_box_height_label
  small_box_height_label = tk.Label(root, text="Height:")
  small_box_height_label.pack()

  global small_box_height_entry
  small_box_height_entry = tk.Entry(root)
  small_box_height_entry.pack()

  global small_box_depth_label
  small_box_depth_label = tk.Label(root, text="Depth:")
  small_box_depth_label.pack()

  global small_box_depth_entry
  small_box_depth_entry = tk.Entry(root)
  small_box_depth_entry.pack()

  global submit_button
  submit_button = tk.Button(root, text="Confirm", command= lambda: on_confirm(instruction_filling_box_text))
  submit_button.pack()

  global result_label
  result_label = tk.Label(root, text="")
  result_label.pack()

  global validation_label
  validation_label = tk.Label(root, fg="red")
  validation_label.pack()

  # global root
  root.mainloop()


def main():
  # dimensions L : longueur, l : largeur, h : hauteur
  # carton = Carton(300, 200, 300) # test 1
  # carton = Carton(310, 235, 250) # test 2
  # carton = Carton(300, 235, 177) # 10p LBE
  carton = Carton(365, 315, 220) # 10p Nutripure
  
  print("Carton")
  # carton.set_dim()
  # presentoire = Boite(200, 99, 99) #test 1
  # Nutripure = 180, 139, 65
  # LBE = 176, 106, 53
  presentoire = Boite(180, 139, 65) # test 2
  print("Presentoire")
  # presentoire.set_dim()

  best_carton = fill_carton([carton], presentoire)
  ui(best_carton.print_placement())

if __name__ == "__main__":
  printf_clear()
  main()
 
