# FAILURE — CARE autoencoder jobs ran out of memory (written at the time)
While we were away the AE jobs on CARE wind farm C (953 sensor columns) were killed by the kernel: one AE fit on a
farm-C turbine peaks at ~4.3 GB (measured: logs/memprobe_ae0.log run, polled RSS), and the queue ran four jobs in
parallel next to PreDist jobs on a 15 GB machine. Later the whole container paused and the runner died (stale
heartbeat). We restarted with three workers, re-queued the killed jobs, and cut the confirmation run to what the
cycle budget allows (decision D-13). Lesson: probe peak memory per dataset before choosing parallelism.
