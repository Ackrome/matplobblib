import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################################################
# Дополнительные функции
#######################################################################################################################
def B2_VISUAL(b, k = 1,lamb_l1=0,lamb_l2=0,num_points=100):
  """
  Визуализирует траекторию изменения весов модели и изолинии L1/L2 регуляризации.

  Args:
      b (pd.DataFrame): DataFrame с двумя столбцами, представляющими
          изменение весов модели на каждой итерации.
      k (int, optional): Масштаб для расширения границ графика. Defaults to 1.
      lamb_l1 (float, optional): Параметр L1 регуляризации (λ). Если не 0,
          будут построены изолинии L1. Defaults to 0.
      lamb_l2 (float, optional): Параметр L2 регуляризации (λ). Если не 0,
          будут построены изолинии L2. Defaults to 0.
      num_points (int, optional): Количество точек для построения сетки
          изолиний. Defaults to 100.
  """
  plt.plot(b[0],b[1])
  plt.grid('ON')
  plt.xlim(-np.max(b) - k,np.max(b) + k)
  plt.ylim(-np.max(b) - k,np.max(b) + k)

  limit = np.max(np.abs(b)) + 1
  # Create a grid of b1 and b2 values
  b1 = np.linspace(-limit, limit, num_points)
  b2 = np.linspace(-limit, limit, num_points)
  B1, B2 = np.meshgrid(b1, b2)

  # Calculate L1 and L2 penalties
  if (lamb_l1!=0):
    L1_penalty = lamb_l1 * (np.abs(B1) + np.abs(B2))
    # Plot L1 regularization isolines with gradient color change
    contour_L1 = plt.contourf(B1, B2, L1_penalty, levels=20, cmap="Oranges_r")
    plt.colorbar(contour_L1, label="L1 Penalty")
    plt.plot(b[0], b[1], "bo-", label="Trajectory")
    plt.title("L1 Regularization Isolines")
    plt.xlabel("$b_1$")
    plt.ylabel("$b_2$")
    plt.grid(True)
    plt.legend()
    
  if (lamb_l2!=0):
    L2_penalty = lamb_l2 * (B1**2 + B2**2)
    contour_L2 = plt.contourf(B1, B2, L2_penalty, levels=20, cmap="Blues_r")
    plt.colorbar(contour_L2, label="L2 Penalty")
    plt.plot(b[0], b[1], "bo-", label="Trajectory")
    plt.title("L2 Regularization Isolines")
    plt.xlabel("$b_1$")
    plt.ylabel("$b_2$")
    plt.grid(True)


  plt.show()
#######################################################################################################################
B2 = [B2_VISUAL]