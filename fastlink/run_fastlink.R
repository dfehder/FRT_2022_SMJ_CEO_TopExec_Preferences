library(readr)
library(fastLink)
library(rjson)

#  Get args
args = commandArgs(trailingOnly=TRUE)
# define region index
rindex <- as.numeric(args[1])
print(rindex)

# load the json referenced in the job file
jsonfile <- args[2]

# get list of regions from json
regions <- fromJSON(file = jsonfile)
print(regions)
# Convert JSON file to a data frame.
region_list <- as.list(regions)

# voter file
voterreg_data_path <- "/project/fehder_718/frt_2021b_data/inter/l2_region_files/"
voter_file <- paste("l2_region_", region_list[[rindex]], ".csv", sep="")
voter_file_path <- paste(voterreg_data_path, voter_file, sep="")
print(voter_file_path)
#exec data
exec_data_path <- "/project/fehder_718/frt_2021b_data/inter/exec_region_files/"
#exec_file <- "exec_region_CS290.csv"
exec_file <- paste("exec_region_", region_list[[rindex]], ".csv", sep="")
exec_file_path <- paste(exec_data_path, exec_file, sep="")

# load data
voterRegData <- read_csv(voter_file_path)
execData <- read_csv(exec_file_path)

# clean data (can be removed on cluster)
voterRegData$name_first <- tolower(voterRegData$name_first)
voterRegData$name_last <- tolower(voterRegData$name_last)

# Define the lambda prior
lam <- (as.numeric(nrow(execData))*.8)/(as.numeric(nrow(voterRegData))*as.numeric(nrow(execData)))
# deal with control flow issues
if (lam < 0.000001) {lam <- lam*100}


# just to see what a print statemtnt looks like on the cluster
print(execData)

# make the subset drops
voterRegData <- subset(voterRegData, yob < 1989)
voterRegData <- subset(voterRegData, hhincome > 100000)

print(nrow(voterRegData))

# run the fastlink code in the wrapper
ff <- fastLink( 
    execData, voterRegData,
    varnames = c("name_first", "name_last", "name_middle_initial", "gender", "yob"),
    stringdist.match = c("name_first", "name_last", "name_middle_initial"),
    numeric.match = c("yob"),
    partial.match = c("name_first", "name_last"),
    threshold.match = .75,
    priors.obj = list(lambda.prior=lam),
    w.lambda = 0.5,
    dedupe.matches = FALSE
)

# Print the Summary
print(summary(ff))

# print the resulting posteriors
print(ff$EM)

# get the matches
matches <- getMatches(
    execData, voterRegData,
    fl.out = ff,
    threshold.match = 0.75
)

# define the match location
out_file <- paste("matches_region_", region_list[[rindex]], ".csv", sep="")
out_path <- "/project/fehder_718/frt_2021b_data/final/matches/"
out_file_path <- paste(out_path, out_file, sep="")

# now merge in the p.gammas for name reweight to avoid open issue #54 using name reweight
# For more info, see (https://github.com/kosukeimai/fastLink/issues/54)

# the number of gammas equal the number of comparison vectors MAKE SURE TO UPDATE WHEN YOU CHANGE MATCH MODEL
# gamvec <- c("gamma.1", "gamma.2", "gamma.3", "gamma.4", "gamma.5", "gamma.6")
gamvec <- c("gamma.1", "gamma.2", "gamma.3", "gamma.4", "gamma.5")

# now merge in the p.gammas to the match file
matches_full <- merge(matches, ff$EM$patterns.w, by=gamvec)


# The next code block follows Appendix S6.3 of Enamorado et al. (2019) but addresses issue open issue #54 using name reweight
# in existing code. for more info, see: https://github.com/kosukeimai/fastLink/issues/54

# now reweight first name
fn <- subset(matches_full, gamma.1 == 2)
msum_fn <- tapply(fn$posterior, fn$name_first, sum)
usum_fn <- tapply(1-fn$posterior, fn$name_first, sum)
fn_merge <- data.frame(cbind(msum_fn, usum_fn))
# now move the names to their own column
fn_merge <- cbind(name_first = rownames(fn_merge), fn_merge)
rownames(fn_merge) <- 1:nrow(fn_merge)
# merge into the main matches file
matches_full <- merge(matches_full, fn_merge, by="name_first", all.x=TRUE)
# cleanup memory
rm("fn", "msum_fn", "usum_fn", "fn_merge")

# now do the same for last name
ln <- subset(matches_full, gamma.2 == 2)
msum_ln <- tapply(ln$posterior, ln$name_last, sum)
usum_ln <- tapply(1-ln$posterior, ln$name_last, sum)
ln_merge <- data.frame(cbind(msum_ln, usum_ln))
# now move the names to their own column
ln_merge <- cbind(name_last = rownames(ln_merge), ln_merge)
rownames(ln_merge) <- 1:nrow(ln_merge)
# merge into the main matches file
matches_full <- merge(matches_full, ln_merge, by="name_last", all.x=TRUE)
rm("ln", "msum_ln", "usum_ln", "ln_merge")

# calculate correction factors (following lines 109-11 in name_reweight function accessed 11/21)
matches_full$rw_fn <- (matches_full$msum_fn*matches_full$p.gamma.j.m)/
    (matches_full$msum_fn*matches_full$p.gamma.j.m + matches_full$usum_fn*matches_full$p.gamma.j.u)
matches_full$rw_fn[is.na(matches_full$rw_fn)] <- 1

matches_full$rw_ln <- (matches_full$msum_ln*matches_full$p.gamma.j.m)/
    (matches_full$msum_ln*matches_full$p.gamma.j.m + matches_full$usum_ln*matches_full$p.gamma.j.u)
matches_full$rw_ln[is.na(matches_full$rw_ln)] <- 1

# now calculate the final posterior
matches_full$posterior_final <- matches_full$rw_ln*matches_full$rw_fn*matches_full$posterior

print("Successfully finished reweight")
## End RW block

# subset to final list 
matches_full_final <- subset(matches_full, posterior_final >= 0.75)

# Now the output
# define the match location
out_file <- paste("matches_region_v3_", region_list[[rindex]], ".csv", sep="")
out_path <- "/project/fehder_718/frt2022a_data/final/matches/"
out_file_path <- paste(out_path, out_file, sep="")

print(out_file_path)

# write the matches
write.csv(matches_full_final, out_file_path)

print("Successfully outputted regional match file")