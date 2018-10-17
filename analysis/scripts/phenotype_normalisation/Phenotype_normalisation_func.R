# functions for transforming phenotypes

# calculate resids of linear model
resids <- function(pheno, age, pc1, pc2, pc3, pc4){
    return(resid(lm(pheno ~ age + (age *  * 2) + pc1 + pc2 + pc3 + pc4, na.action = na.exclude)))
}

# inverse normalise distribution
INVN <- function(x){
    return(qnorm((rank(x, na.last = "keep") - 0.5) / sum(! is.na(x))))
}

###

# Can use a function like this to loop through and normalise phenotypes. set up for case control. non case control data can be only sex split. 

for (i in c("BMI", "INS_FAST", "HBA1C_MMOL", "GAD_AB", "SERUM_CREATININE", "ADIPONECTIN", "LEPTIN", "CHOL",
            "LDL_CALCULATED", "HDL", "TG", "HEIGHT_CM", "WEIGHT_KG", "WAISTC_CM", "SBP", "DBP", "eGFR1")) {
    mn_ca[, paste(i , "_ADJ", sep = "")] <- INVN(resids(mn_ca[, i], mn_ca$AGE_T2D_DIAGNOSIS, mn_ca$PC1, mn_ca$PC2, mn_ca$PC3, mn_ca$PC4))
    mn_cl[, paste(i , "_ADJ", sep = "")] <- INVN(resids(mn_cl[, i], mn_cl$AGE_T2D_DIAGNOSIS, mn_cl$PC1, mn_cl$PC2, mn_cl$PC3, mn_cl$PC4))
    wmn_cl[, paste(i , "_ADJ", sep = "")] <- INVN(resids(wmn_cl[, i], wmn_cl$AGE_T2D_DIAGNOSIS, wmn_cl$PC1, wmn_cl$PC2, wmn_cl$PC3, wmn_cl$PC4))
    try(wmn_ca[, paste(i , "_ADJ", sep = "")] <- INVN(resids(wmn_ca[, i], wmn_ca$AGE_T2D_DIAGNOSIS, wmn_ca$PC1, wmn_ca$PC2, wmn_ca$PC3, wmn_ca$PC4)), silent = TRUE)
}

# calculate eGFR

EGFR <- function(df, cr, Age, Sex){
    for (i in 1 : nrow(df)) {
        if (! (is.na(df[i, cr]))) {
            if (as.character(df[i, Sex]) == 2) {
                df[i, "eGFR1"] <- (141 *
                    (min(((df[i, cr] / 88.4) / .7), 1) *  * - 0.329) *
                    (max(((df[i, cr] / 88.4) / .7), 1) *  * - 1.209) *
                    (0.993 *  * df[i, Age]) *
                    1.018)
            }
            else if (as.character(df[i, Sex]) == 1) {
                df[i, "eGFR1"] <- (141 *
                    (min(((df[i, cr] / 88.4) / .9), 1) *  * - 0.411) *
                    (max(((df[i, cr] / 88.4) / .9), 1) *  * - 1.209) *
                    (0.993 *  * df[i, Age]))
            }
            else {
                df[i, "eGFR1"] <- "NA"
            }
        }
    }
    return(df)
}
df1 <- EGFR(df = df, cr = "SERUM_CREATININE", Age = "Age", Sex = "Sex")



