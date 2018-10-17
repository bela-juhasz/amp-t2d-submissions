# some functions i use to make phenotype distribution plots, QQ plots and Manhattan plots

pheno_dist <- function(pheno){
    nums <- unlist(lapply(pheno, is.numeric)) # NUMERIC COLUMNS only need to add categorical
    df <- pheno[, nums]
    for (i in (3 : length(df))) {
        mypath <- file.path(paste("./", colnames(df)[i], ".png", sep = ""))
        png(file = mypath)
        mytitle <- paste(colnames(df)[i], "Distribution", sep = " ")
        hist(as.numeric(unlist(df[i])), breaks = 120, main = mytitle, probability = TRUE, col = "gray", border = "white")
        d <- density(na.omit(as.numeric(unlist(df[i]))))
        lines(d, col = "blue")
        rug(as.numeric(unlist(df[i])), col = "red")
        dev.off()
    }
}


######################################
#### MH + QQ script.
######################################

library("ggplot2")
library("qqman")
## github func


gg_qqplot <- function(df, ci = 0.95, handle) {
    N <- length(df)
    df <- data.frame(
    observed = - log10(sort(df)),
    expected = - log10(1 : N / N),
    clower = - log10(qbeta(ci, 1 : N, N - 1 : N + 1)),
    cupper = - log10(qbeta(1 - ci, 1 : N, N - 1 : N + 1))
    )
    log10Pe <- expression(paste("Expected -log"[10], plain(P)))
    log10Po <- expression(paste("Observed -log"[10], plain(P)))
    ggplot(df) +
        geom_point(aes(expected, observed), shape = 1, size = 3) +
        geom_abline(intercept = 0, slope = 1, alpha = 0.5) +
        geom_line(aes(expected, cupper), linetype = 2) +
        geom_line(aes(expected, clower), linetype = 2, color = 'red') +
        xlab(log10Pe) +
        ylab(log10Po) +
        ggtitle(paste(handle[3], " QQ-plot", sep = " "))
}

#  GRM here is the genetic relationship snps association the p values seem to be very close to the projected.
# (GRM number of assocs ~1M full dosage projected is 16M)
files <- list.files(pattern = "*.GRM", full.names = T, recursive = FALSE)
for (i in files) {
    handle <- unlist(strsplit(i, "[.]"))
    print(paste("Reading", handle[3], "Summary Statistics", sep = " "))
    df <- read.table(i, h = T) # impotant to only take additive model p values
    print("Reading Complete")
    print("Renamin p-value column")
    names(df)[11] <- "P"
    print("Making Manhattan plot")
    png(paste("./Hoorn.", handle[3], ".mh.png", sep = ""))
    manhattan(df, main = paste(handle[3], ".mh.png", sep = ""))
    print(paste(handle[3], "Manhattan plot is complete", sep = " "))
    #  png(paste("./Hoorn.",handle[3],".qq.png",sep=""))
    print(paste("Making", handle[3], "QQ plot", sep = " "))
    plot <- gg_qqplot(df$P, ci = 0.95, handle = handle)
    print(paste(handle[3], "QQ plot is complete", sep = " "))
    print("Saving plot")
    print(paste("./Hoorn.", handle[3], ".qq.png", sep = ""))
    ggsave(filename = paste("./Hoorn.", handle[3], ".qq.png", sep = ""), plot = last_plot(), device = NULL, width = 16, height = 9, dpi = 100)
    dev.off()
    print(paste(handle[3], " is complete. Next Phenotype", sep = " "))
}
