import numpy as np
import pytransform3d.rotations as pr
from scipy.spatial.transform import Rotation as R

#-----------------------------------------------------------------------------------------------------------------------
#
def convert_tensor(C):

    voigt_map = {(0, 0): 0, (1, 1): 1, (2, 2): 2, (0, 1): 3, (1, 0): 3, (0, 2): 4, (2, 0): 4, (1, 2): 5, (2, 1): 5}

    if C.shape == (6, 6):  # 2D -> 4D
        C4 = np.zeros((3, 3, 3, 3))
        for (i, j), m in voigt_map.items():
            for (k, l), n in voigt_map.items():
                C4[i, j, k, l] = C[m, n]
        return C4
    if C.shape == (3, 3, 3, 3):  # 4D -> 2D
        C2 = np.zeros((6, 6))
        for (i, j), m in voigt_map.items():
            for (k, l), n in voigt_map.items():
                C2[m, n] = C[i, j, k, l]
        return C2

def transversely_isotropic(elastic_paras):

    # Define equivalent parameters for transverse isotropy
    E11, E22, mu12, mu23, G12 = elastic_paras
    E33, mu13, mu32, G13 = E22, mu12, mu23, G12
    mu21, mu31 = E22 * mu12 / E11, E33 * mu13 / E11
    G23 = 0.5 * E22 / (1 + mu23)  # Shear modulus in the transverse plane

    # compliance matrix S (6×6)
    S = np.zeros((6, 6))
    S[0:3, 0:3] = [[1 / E11, -mu21 / E22, -mu31 / E33], [-mu21 / E22, 1 / E22, -mu32 / E33],
        [-mu31 / E33, -mu32 / E33, 1 / E33]]
    S[3:6, 3:6] = np.diag([1 / G12, 1 / G13, 1 / G23])
    return convert_tensor(np.linalg.inv(S))

def elas_paras2abaqus(elastic_stiff):
    #
    indices = [
        (0, 0, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1), (0, 0, 2, 2), (1, 1, 2, 2), (2, 2, 2, 2), (0, 0, 0, 1), (1, 1, 0, 1),
        (2, 2, 0, 1), (0, 1, 0, 1), (0, 0, 0, 2), (1, 1, 0, 2), (2, 2, 0, 2), (0, 1, 0, 2), (0, 2, 0, 2),
        (0, 0, 1, 2), (1, 1, 1, 2), (2, 2, 1, 2), (0, 1, 1, 2), (0, 2, 1, 2), (1, 2, 1, 2)]
    return np.array([elastic_stiff[i, j, k, l] for i, j, k, l in indices])


def rotation_from_phi_theta(phi, theta):
    v = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
    x0 = np.array([1,0,0])
    rotation_matrix = R.align_vectors([v], [x0])[0]
    return rotation_matrix.as_matrix()

#-----------------------------------------------------------------------------------------------------------------------
#
composite_type = 'woven_composites' # 'braided_composites_2'  #
#
if composite_type == 'braided_composites_1': # vyf=0.7
    Width, Thick, LayerT = 4.0, 4.0, 0.2 / 25.0
    Height = Width
    igamma = np.arctan(np.sqrt(2.0)) * 180 / np.pi
    # phi, theta, psi for matrix_from_euler
    ori_angles = - np.array([[135, igamma, 0], [225, igamma, 0], [45, igamma, 0], [315, igamma, 0]]) * np.pi / 180.
    elastic_paras_0 = np.array([350000, 350000, 0.2, 0.2, 145800])
    elastic_paras_1 = np.array([259440, 49393, 0.11936, 0.35877, 11652])
    alpha_paras_0 = np.diag([1.9, 1.9, 1.9])
    alpha_paras_1 = np.diag([0.6633, 4.9616, 4.9616])
    kappa_paras_0 = np.diag([70.0, 70.0, 70.0])
    kappa_paras_1 = np.diag([26.467, 13.006, 13.006])

    ro_matrices = [rotation_from_phi_theta(phi, theta) for phi, theta, _ in ori_angles]

    elastic_stiff_0 = transversely_isotropic(elastic_paras_0)
    elastic_stiff_1 = transversely_isotropic(elastic_paras_1)
    elastic_stiff_1_transformed = [np.einsum('ai, bj, ck, dl, abcd -> ijkl', R, R, R, R, elastic_stiff_1) for R in
                                   ro_matrices]
    for i, C in enumerate([elastic_stiff_0] + elastic_stiff_1_transformed):
        np.savetxt(f'braided4_fft_elastic_stiff_{i}.txt', convert_tensor(C), delimiter=',', fmt="%.3f")

    alpha_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, alpha_paras_1) for R in ro_matrices]
    for i, A in enumerate([alpha_paras_0] + alpha_paras_1_transformed):
        np.savetxt(f'braided4_abaqus_alpha_{i}.txt',
                   np.array([A[0, 0], A[1, 1], A[2, 2], A[0, 1], A[0, 2], A[1, 2]]).reshape(1, -1), delimiter=',',
                   fmt="%.3f")

    kappa_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, kappa_paras_1) for R in ro_matrices]
    kappa_0 = [np.zeros((3, 3))]
    for i, K in enumerate([kappa_paras_0] + kappa_paras_1_transformed):
        np.savetxt(f'braided4_abaqus_kappa_{i}.txt',
                   np.array([K[0, 0], K[0, 1], K[1, 1], K[0, 2], K[1, 2], K[2, 2]]).reshape(1, -1),
                   delimiter=',', fmt="%.3f")

elif composite_type == 'braided_composites_2':  # vyf=0.7
    alpha = 45.0
    sb, r = 1.0, 2.0
    shift_dis = 0.06
    #
    width = (4 + 2 * r) * sb / np.cos(alpha / 180 * np.pi)
    thickness = (4 + 2 * r) * sb / np.sin(alpha / 180 * np.pi)
    height = thickness
    rve_size = np.array([width + shift_dis, thickness + shift_dis, height + shift_dis])
    igamma = np.arctan(4 * (2 + r) * sb / (height * np.sin(2.0 * alpha / 180 * np.pi))) * 180 / np.pi
    #
    ori_angles = - np.array(
        [[225, igamma, 0], [135, igamma, 0], [315, igamma, 0], [45, igamma, 0], [0, 0, 0]]) * np.pi / 180.
    elastic_paras_0 = np.array([350000, 350000, 0.2, 0.2, 145800])
    elastic_paras_1 = np.array([259440, 49393, 0.11936, 0.35877, 11652])
    alpha_paras_0 = np.diag([1.9, 1.9, 1.9])
    alpha_paras_1 = np.diag([0.6633, 4.9616, 4.9616])
    kappa_paras_0 = np.diag([70.0, 70.0, 70.0])
    kappa_paras_1 = np.diag([26.467, 13.006, 13.006])

    ro_matrices = [rotation_from_phi_theta(phi, theta) for phi, theta, _ in ori_angles]

    elastic_stiff_0 = transversely_isotropic(elastic_paras_0)
    elastic_stiff_1 = transversely_isotropic(elastic_paras_1)
    elastic_stiff_1_transformed = [np.einsum('ai, bj, ck, dl, abcd -> ijkl', R, R, R, R, elastic_stiff_1)
                                   for R in ro_matrices]
    for i, C in enumerate([elastic_stiff_0] + elastic_stiff_1_transformed):
        np.savetxt(f'braided5_abaqus_elastic_stiff_{i}.txt', elas_paras2abaqus(C).reshape(1, -1),
                   delimiter=',', fmt="%.3f")

    alpha_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, alpha_paras_1) for R in ro_matrices]
    for i, A in enumerate([alpha_paras_0] + alpha_paras_1_transformed):
        np.savetxt(f'braided5_abaqus_alpha_{i}.txt',
                   np.array([A[0, 0], A[1, 1], A[2, 2], A[0, 1], A[0, 2], A[1, 2]]).reshape(1, -1),
                   delimiter=',',
                   fmt="%.3f")

    kappa_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, kappa_paras_1) for R in ro_matrices]
    kappa_0 = [np.zeros((3, 3))]
    for i, K in enumerate([kappa_paras_0] + kappa_paras_1_transformed):
        np.savetxt(f'braided5_abaqus_kappa_{i}.txt',
                   np.array([K[0, 0], K[0, 1], K[1, 1], K[0, 2], K[1, 2], K[2, 2]]).reshape(1, -1),
                   delimiter=',', fmt="%.3f")

else: # vyf = 0.65
    # phi, theta, psi for matrix_from_euler
    ori_angles = np.array([[0, 90, 0], [0, 0, 0]]) * np.pi / 180. # woven
    elastic_paras_0 = np.array([3450, 3450, 0.37, 0.37, 1260])
    elastic_paras_1 = np.array([48335, 18297, 0.2515, 0.4187, 7408])
    alpha_paras_0 = np.diag([69.0, 69.0, 69.0])
    alpha_paras_1 = np.diag([7.795, 23.11, 23.11])
    kappa_paras_0 = np.diag([0.19, 0.19, 0.19])
    kappa_paras_1 = np.diag([0.736, 0.55693, 0.55693])

    ro_matrices = [rotation_from_phi_theta(phi, theta) for phi, theta, _ in ori_angles]

    elastic_stiff_0 = transversely_isotropic(elastic_paras_0)
    elastic_stiff_1 = transversely_isotropic(elastic_paras_1)
    elastic_stiff_1_transformed = [np.einsum('ai, bj, ck, dl, abcd -> ijkl', R, R, R, R, elastic_stiff_1) for R in ro_matrices]
    for i, C in enumerate([elastic_stiff_0] + elastic_stiff_1_transformed):
        np.savetxt(f'woven_abaqus_elastic_stiff_{i}.txt', elas_paras2abaqus(C).reshape(1, -1), delimiter=',', fmt="%.3f")

    alpha_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, alpha_paras_1) for R in ro_matrices]
    for i, A in enumerate([alpha_paras_0] + alpha_paras_1_transformed):
        np.savetxt(f'woven_abaqus_alpha_{i}.txt', np.array([A[0,0], A[1,1], A[2,2], A[0,1], A[0,2], A[1,2]]).reshape(1, -1), delimiter=',', fmt="%.3f")

    kappa_paras_1_transformed = [np.einsum('ai, bj, ab -> ij', R, R, kappa_paras_1) for R in ro_matrices]
    kappa_0 = [np.zeros((3, 3))]
    for i, K in enumerate([kappa_paras_0] + kappa_paras_1_transformed):
        np.savetxt(f'woven_abaqus_kappa_{i}.txt', np.array([K[0, 0], K[0, 1], K[1, 1], K[0, 2], K[1, 2], K[2, 2]]).reshape(1, -1),
                   delimiter=',', fmt="%.3f")