public class MichaelisMentenKinetics {
    public static double calculateVelocity(double vMax, double km, double substrateConcentration) {
        if (substrateConcentration < 0) return 0.0;
        return (vMax * substrateConcentration) / (km + substrateConcentration);
    }

    public static double calculateKcat(double vMax, double totalEnzymeConcentration) {
        if (totalEnzymeConcentration <= 0) return 0.0;
        return vMax / totalEnzymeConcentration;
    }
}