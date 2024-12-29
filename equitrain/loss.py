import math
import torch

class GenericLoss(torch.nn.Module):

    def __init__(
        self,
        energy_weight = 1.0,
        force_weight  = 1.0,
        stress_weight = 0.0,
        loss_energy_per_atom = True,
        **args
        ):

        super().__init__()

        # TODO: Allow to select other los functions with args
        self.loss_energy = torch.nn.L1Loss()
        self.loss_forces = torch.nn.L1Loss()
        self.loss_stress = torch.nn.L1Loss()

        # TODO: Use register_buffer instead
        self.energy_weight = energy_weight
        self.force_weight  = force_weight
        self.stress_weight = stress_weight

        self.loss_energy_per_atom = loss_energy_per_atom


    def compute_weighted_loss(self, energy_loss, force_loss, stress_loss):
        result = 0.0
        # handle initial values correctly when weights are zero, i.e. 0.0*Inf -> NaN
        if energy_loss is not None and (not math.isinf(energy_loss) or self.energy_weight > 0.0):
            result += self.energy_weight * energy_loss
        if force_loss is not None and (not math.isinf(force_loss) or self.force_weight > 0.0):
            result += self.force_weight * force_loss
        if stress_loss is not None and (not math.isinf(stress_loss) or self.stress_weight > 0.0):
            result += self.stress_weight * stress_loss

        return result


    def forward(self, y_pred, y_true):

        e_true = y_true.y
        f_true = y_true['force']
        s_true = y_true['stress']

        e_pred = y_pred['energy']
        f_pred = y_pred['forces']
        s_pred = y_pred['stress']

        loss_e = None
        loss_f = None
        loss_s = None

        if self.energy_weight > 0.0:
            loss_e = self.loss_energy(e_pred, e_true)
        if self.force_weight > 0.0:
            loss_f = self.loss_forces(f_pred, f_true)
        if self.stress_weight > 0.0:
            loss_s = self.loss_stress(s_pred, s_true)

        loss = self.compute_weighted_loss(loss_e, loss_f, loss_s)

        return { 'total': loss, 'energy': loss_e, 'forces': loss_f, 'stress': loss_s }
