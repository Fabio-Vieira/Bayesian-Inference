x <- rnorm(15, mean = 5.7, sd = sqrt(16))
mean(x)
var(x)

init <- list()
init$mu <- 0.00
init$sig2 <- 1.00

prior <- list()
prior$m.0 <- 4.00
prior$sig2.mu <- 10.00
prior$a <- 1
prior$b <- 3

update.mu <- function(sig2, x, sig2.mu, m.0){
	n <- length(x)
	x.bar <- mean(x)

	sig2.mu.post <- 1/(n/sig2 + 1/sig2.mu)
	m.0.post <- sig2.mu.post * (sum(x)/sig2 + m.0/sig2.mu)

	rnorm(1, m.0.post, sig2.mu.post)
}

update.sig <- function(a, b, x, mu){
	n <- length(x)
	a.post <- n/2 + a
	sumsq <- sum((x - mu)^2)
	b.post <- sumsq/2 + b

	1/rgamma(1, a.post, b.post)
}

n_iter <- 50000
mu_out <- numeric(n_iter)
sig2_out <- numeric(n_iter)

mu_now <- init$mu
sig2_now <- init$sig2

for(i in 1:n_iter){
	mu_now <- update.mu(sig2_now, x, prior$sig2.mu, prior$m.0)
	sig2_now <- update.sig(prior$a, prior$b, x, mu_now)

	mu_out[i] <- mu_now
	sig2_out[i] <- sig2_now
}

post <- cbind(mu = mu_out, sig2 = sig2_out)
post.burnin <- post[5001:50000,]

apply(post.burnin, 2, mean)

library(coda)
plot(as.mcmc(post.burnin[,1:2]))

quantile(post.burnin[,1], c(.05, .95))
quantile(post.burnin[,2], c(.05, .95))

HPDinterval(as.mcmc(post.burnin[,1]), prob = .95)
HPDinterval(as.mcmc(post.burnin[,2]), prob = .95)



