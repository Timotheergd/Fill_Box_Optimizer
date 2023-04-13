def printf_clear(log_file):
  # Clear the log file
  with open(log_file, 'w') as f:
    f.write('Hi, this is the log file.\n')

def printf(log_file, *text):
  # Write the text in the log file
  with open(log_file, 'a', newline=None) as f:
    for t in text:
      f.write(str(t))
    f.write("\n")

class Box:
  """
  This class is a 3d object, a parallelepiped
  This is use to define littles boxes that we put on a pallet (class )
  """

  def __init__(self, _L=1, _w=1, _h=1):
    self.L = _L # Lenght
    self.w = _w # Width
    self.h = _h # Height

  def ask_dim(self):
    # Ask sizes of the object to the user
    print("Please enter the following values of the box :")
    self.L = int(input("Lenght : "))
    self.w = int(input("Width : "))
    self.h = int(input("Height : "))

  def get_dim(self):
    # return the dimensions of the box
    return [self.L, self.w, self.h]
  
  def get_volume(self):
    # return the volume of the box
    return self.L*self.w*self.h


class Pallet(Box):
  """
  This class can contain boxes. The goal is to put as much Box as possible in the pallet. 
  """

  def __init__(self, _L=1, _w=1, _h=1):
    Box.__init__(self, _L, _w, _h)
    self.content = [] # Content of the pallet. This is a list filled by [rotation, nb_L, nb_w, nb_h] : nb_L*nb_w*nb*h boxes are position with the rotation
    self.nb_box = 0   # this keep up how many boxes are in the pallet

  def add_box(self, rotation, nb_L, nb_w, nb_h):
    """
    Add boxes to the pallet.
    There are nb_L box in the Lenght, nb_w boxes in the width and nb_h boxes in the height.
    The rotation is define by the rotation variable.
    """
    if (nb_L*nb_w*nb_h) > 0: # if there are boxes to fit in the pallet
      merged=False
      for i in range(len(self.content)):
        if rotation==self.content[i][0]: # if boxes where already put with the same rotation
          if (nb_L * nb_w * nb_h) > (self.content[i][1] * self.content[i][2] * self.content[i][3]): # if the number of boxes to fit is greater than the number of boxes already there
            self.content[i] = [rotation, nb_L, nb_w, nb_h] # update of the number of boxes in this rotation
            # And update of the number of boxes in the pallet
            self.nb_box -= self.content[i][1] * self.content[i][2] * self.content[i][3]
            self.nb_box += nb_L * nb_w * nb_h
          merged=True
      if not merged: # if none of the boxes are in the same rotation
        # Add boxes to the content 
        self.content.append([rotation, nb_L, nb_w, nb_h])
        self.nb_box += nb_L * nb_w * nb_h

  def remove_box(self, rotation, nb_L, nb_w, nb_h, debug=False, log_file=".log"):
    """
    Remove boxes from the pallet from the rotation and the number of boxes in the lenght, width and height
    """
    if len(self.content) == 0: 
      return 
    try:
      self.content.remove([rotation, nb_L, nb_w, nb_h])
      self.nb_box -= nb_L * nb_w * nb_h
    except:
      if debug:
        printf(log_file, "failed to remove boites from the pallet"+"*"*10)
        printf(log_file, f"{self.content=}")

  def __gt__(self, other):
    return self.nb_box > other.nb_box

  def copy(self):
    new_box = Pallet(self.L, self.w, self.h)
    new_box.content = self.content[:]
    new_box.nb_box = self.nb_box
    return new_box

  def __str__(self):
    return "Pallet :\ndimensions : " + str(self.L) + "x" + str(self.w) + "x" + str(self.h) + "\nnb_boxes : " + str(self.nb_box) + "\ncontent : " + str(self.content)

  def combine(self, other):
    for i in range(len(other.content)):
      self.add_box(other.content[i][0], other.content[i][1], other.content[i][2], other.content[i][3])

  def print_way_fill(self, debug=False):
    """
    Explain how you need to rotate the boxes in the pallet
    """
    text_to_print=""
    nb_step = 1
    text_to_print+=f"Way to fill the pallet :\n{nb_step}. Position the pallet with the long side facing you.\n"
    if debug: print(f"Way to fill the pallet :\n{nb_step}. Position the pallet with the long side facing you.")
    for step in self.content:
      nb_step+=1
      rotation_text=""
      if step[0]==1:
          rotation_text="flat along the length of the pallet"
      elif step[0]==2:
          rotation_text="vertically on the long edge, along the length of the pallet"
      elif step[0]==3:
          rotation_text="flat along the width of the pallet"
      elif step[0]==4:
          rotation_text="vertically on the short edge, parallel to the length of the pallet"
      elif step[0]==5:
          rotation_text="vertically on the long edge, along the width of the pallet"
      elif step[0]==6:
          rotation_text="vertically on the short edge, parallel to the width of the pallet"
      
      if debug: print(f"{nb_step}. Position (L*w*h) {step[1]}*{step[2]}*{step[3]} = {step[1]*step[2]*step[3]} box(es) " + rotation_text)
      text_to_print+=f"{nb_step}. Position {step[1]*step[2]*step[3]} box(es) " + rotation_text + "\n"
    
    return text_to_print

  def print_total(self, debug=False):
    """
    Return text : how many boxes are positioned in the pallet ?, with the number in an other variable, to print it in bold later
    """
    if debug:
      print(f"You have now placed {self.nb_box} box(es) in the pallet")
    text_to_print_start=f"You have now placed"
    text_to_print_bold=f" {self.nb_box} "
    text_to_print_end=f"box(es) in the pallet\n"
    return (text_to_print_start, text_to_print_bold, text_to_print_end)

def possibilities(dimensions):
  """
  Return all arragement of the list
  Each arrangement is associated with a number, this correspond to the rotation
  [L, w, h] -> 1
  [L, h, w] -> 2
  [w, L, h] -> 3
  [w, h, L] -> 4
  [h, L, w] -> 5
  [h, w, L] -> 6
  """
  p = []
  for i in range(3):
    k = [0, 1, 2]
    n1 = k[i]
    k.remove(n1)
    for j in range(2):
      n2 = k[j % 2]
      n3 = k[(j + 1) % 2]
      a = [dimensions[n1], dimensions[n2], dimensions[n3]]
      p.append(a)
  return p

def fill_pallet(_pallet,
                box,
                fill_rest=True,
                _previous_pallet=Pallet(),
                debug=False,
                log_file=".log"):
  best_pallet = Pallet()               
  
  n = 0  # to get track of the current dimension
  for dim in possibilities(box.get_dim()):
    pallet = _pallet.copy()
    pallet_fill_rest = []
    previous_pallet = _previous_pallet.copy()  

    if debug:
      if (fill_rest): printf(log_file, "\n" * 2 + "-+*+-" * 10 + "________base")
      else: printf(log_file, "________rest")
      printf(log_file, dim, " in ", pallet.get_dim())

    n += 1
    if debug: printf(log_file, "n=", n)

    # Calculate the number of boxes we can fit on the lenght(l), width(w), height(h)
    nb_L = pallet.L // dim[0]
    L = dim[0] * nb_L

    nb_w = pallet.w // dim[1]
    w = dim[1] * nb_w

    nb_h = pallet.h // dim[2]
    h = dim[2] * nb_h

    # Calculate the space left on the sides
    L_r, w_r, h_r = 0, 0, 0
    if not nb_L*nb_w*nb_h == 0:
      L_r = pallet.L - L
      w_r = pallet.w - w
      h_r = pallet.h - h

    pallet.add_box(n, nb_L, nb_w, nb_h)

    previous_pallet.combine(pallet)

    if debug: 
      printf(log_file, "nb box=", nb_L, "x", nb_w, "x", nb_h, " =", nb_L * nb_w * nb_h)
      printf(log_file, "nb box in pallet=", nb_L, "x", nb_w, "x", nb_h, " =", pallet.nb_box)
      printf(log_file, "total=", previous_pallet.nb_box)
      printf(log_file, "total=", previous_pallet.content)
      printf(log_file, "total=", L, "x", w, "x", h)
      printf(log_file, "rest=", L_r, "x", w_r, "x", h_r)

    # Check if the pallet is better than the previous
    if previous_pallet > best_pallet:
      best_pallet = previous_pallet.copy()

    # Fill the gaps by creating new virtual pallets
    if (fill_rest):
      pallet_L = Pallet(L_r, pallet.w, pallet.h)
      pallet_l = Pallet(pallet.L, w_r, pallet.h)
      pallet_h = Pallet(pallet.L, pallet.w, h_r)
      pallet_fill_rest.append(pallet_L)
      pallet_fill_rest.append(pallet_l)
      pallet_fill_rest.append(pallet_h)
      if debug: 
        printf(log_file, "="*10 + "\nPallets to fill \n" + "="*10)
        for c in pallet_fill_rest:
          printf(log_file, c)
      for pallet in pallet_fill_rest:
        best_little_pallet_fill = fill_pallet(pallet, box, False, previous_pallet.copy(), debug, log_file)
        previous_pallet.combine(best_little_pallet_fill)

        if previous_pallet > best_pallet:
          best_pallet = previous_pallet.copy()

    pallet.remove_box(n, nb_L, nb_w, nb_h, log_file, debug)

  if debug: 
    printf(log_file, "\n\n\n")
    printf(log_file, "*" * 20)
    printf(log_file, "best pallet=", best_pallet.nb_box)
    printf(log_file, "content=", best_pallet.content)
    printf(log_file, "*" * 20)
  return best_pallet.copy()

import tkinter as tk

def validate_sizes(debug=False):
    """
    Update the ui after confirm to explain how to fill the pallet
    """
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

    pallet = Pallet(int(big_box_width), int(big_box_depth), int(big_box_height))
    box = Box(int(small_box_width), int(small_box_depth), int(small_box_height))
    best_pallet = fill_pallet(pallet, box, debug=debug, log_file=log_file)

    global root
    
    root.title("Result")
    root.geometry("1000x500")
    global result_label
    
    result_label.configure(state="normal")
    result_label.delete("1.0",tk.END)
    result_label.insert("1.0", f"Size of the pallet: {big_box_size}\nSize of the boxes: {small_box_size}\n\n" + str(best_pallet.print_way_fill()))
    end_pos = int(result_label.index("end").split(".")[0])

    text_start, text_bold, text_end = best_pallet.print_total(debug)
    
    result_label.insert("end", text_start, ('normal'))
    result_label.insert("end", text_bold, "Arial bold 12")
    result_label.insert("end", text_end, ('normal'))
    result_label.tag_add('text_bold',f"{int(end_pos)-1}.{len(text_start)}", f"{int(end_pos)-1}.{len(text_start)+len(text_bold)+14}")
    result_label.tag_config('text_bold', font='arial 11 bold')

    result_label.tag_configure("center", justify='center')
    result_label.tag_add("center", "1.0", "end")

    result_label.configure(state="disabled")
    result_label.pack(fill="both")
    
    validation_label.config(text="")
    
    return True

def on_confirm(debug=False):
    if validate_sizes(debug):
        print("Box sizes confirmed")

def ui(debug=False):
  """
  Create the UI to ask for the dimensions of the pallet and the boxes
  """

  global root
  root = tk.Tk()
  root.title("Box Size Input")
  root.geometry("400x350")

  global big_box_label
  big_box_label = tk.Label(root, text="Pallet", font="Verdana 11 underline") 
  big_box_label.pack()

  global big_box_width_label
  big_box_width_label = tk.Label(root, text="Lenght:")
  big_box_width_label.pack()

  global big_box_width_entry
  big_box_width_entry = tk.Entry(root)
  big_box_width_entry.pack()

  global big_box_depth_label
  big_box_depth_label = tk.Label(root, text="Width:")
  big_box_depth_label.pack()

  global big_box_depth_entry
  big_box_depth_entry = tk.Entry(root)
  big_box_depth_entry.pack()

  global big_box_height_label
  big_box_height_label = tk.Label(root, text="Height:")
  big_box_height_label.pack()

  global big_box_height_entry
  big_box_height_entry = tk.Entry(root)
  big_box_height_entry.pack()

  global small_box_label
  small_box_label = tk.Label(root, text="Box", font="Verdana 11 underline")
  small_box_label.pack()

  global small_box_width_label
  small_box_width_label = tk.Label(root, text="Lenght:")
  small_box_width_label.pack()

  global small_box_width_entry
  small_box_width_entry = tk.Entry(root)
  small_box_width_entry.pack()

  global small_box_depth_label
  small_box_depth_label = tk.Label(root, text="Width:")
  small_box_depth_label.pack()

  global small_box_depth_entry
  small_box_depth_entry = tk.Entry(root)
  small_box_depth_entry.pack()

  global small_box_height_label
  small_box_height_label = tk.Label(root, text="Height:")
  small_box_height_label.pack()

  global small_box_height_entry
  small_box_height_entry = tk.Entry(root)
  small_box_height_entry.pack()

  global submit_button
  submit_button = tk.Button(root, text="Confirm", command=lambda:on_confirm(debug))
  submit_button.pack()

  global result_label
  result_label = tk.Text(root)
  result_label.pack()

  global validation_label
  validation_label = tk.Label(root, fg="red")
  validation_label.pack()

  root.mainloop()

def main(log_file, debug=False):
  ui(debug)

def test_one_config(pallet, box, nb_boites_theorique, n, debug=False, log_file=".log"):
  if (debug): printf(log_file, "\n"*3+"+-"*20+"\n"*3)
  best_pallet = fill_pallet(pallet, box, debug, log_file)
  best_pallet.print_way_fill(True)
  if best_pallet.nb_box == nb_boites_theorique:
    printf(log_file, u"\u2705" + f" TEST {n} PASSED with {100*best_pallet.nb_box*box.get_volume()//pallet.get_volume()} % of the volume filled\n")
  else:
    printf(log_file, u"\u274C" + f" TEST {n} FAILED with {100*best_pallet.nb_box*box.get_volume()//pallet.get_volume()} % of the volume filled : nb_box={best_pallet.nb_box}\n"+best_pallet.print_way_fill())

def num_test():
    if hasattr(num_test, "num"):
        num_test.num += 1 # increment if not first call
    else:
        num_test.num = 1 # initialize on first call
    return num_test.num

def test_all(debug=False):
  # This tests are verified by a human.

  printf(log_file, "*"*20+"\n TESTS \n"+"*"*20)
  
  test_one_config(Pallet(300, 235, 177), Box(176, 106, 53), 10, num_test(), debug, log_file)
  test_one_config(Pallet(365, 315, 220), Box(180, 139, 65), 13, num_test(), debug, log_file)
  test_one_config(Pallet(500, 400, 300), Box(400, 300, 100), 5, num_test(), debug, log_file)
  test_one_config(Pallet(500, 400, 400), Box(400, 300, 100), 6, num_test(), debug, log_file)
  test_one_config(Pallet(600, 400, 400), Box(400, 300, 100), 8, num_test(), debug, log_file)
  test_one_config(Pallet(310, 235, 250), Box(180, 139, 65), 8, num_test(), debug, log_file)

if __name__ == "__main__":
  log_file = 'fill_box_optimiser.log'
  printf_clear(log_file)
  # test_all(debug=False)
  main(log_file, debug=False)
 
