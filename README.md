# Open Traffic Generator examples

## Overview 

[OTG examples](https://github.com/open-traffic-generator/otg-examples) repository is a great way to get started with [Open Traffic Generator API](https://otg.dev). It features a collection of software-only network labs ranging from very simple to more complex. To setup network labs in software we use containerized or virtualized NOS images.

## OTG Tools

There are several implementations of OTG API. Each example uses one of the following:

* [Ixia-c TE](https://otg.dev/implementations/#ixia-c): Ixia-c Traffic Engine
* [Ixia-c-one](https://github.com/open-traffic-generator/ixia-c/blob/main/docs/deployments.md#deploy-ixia-c-one-using-containerlab): a single-container package of Ixia-c Traffic Engine for Containerlab
* [KENG TE](https://otg.dev/implementations/#keng): Keysight Elastic Network Generator – Traffic Engine
* [KENG TE+PE](https://otg.dev/implementations/#keng): Keysight Elastic Network Generator – Traffic and Protocol Engines

## Device Under Test

Many network vendors provide versions of their Network Operating Systems as a CNF or VNF. To make OTG Examples available for a widest range of users, our labs use open-source or freely available NOSes like [FRR](https://frrouting.org/). Replacing FRR with a container from a different vendor is a matter of modifying one of the lab examples.

Some examples don't have any DUT and use back-2-back connections between Test Ports. These are quite useful to make sure the Traffic Generator part works just fine by itself, before introducing a DUT.

## OTG Client

A job of an OTG Client is to communicating with a Traffic Generator via the OTG API and request it to perform tasks such as applying a configuration, starting protocols, running traffic, collecting metrics. Each example uses one (or sometimes more) of the following OTG Clients:

* [`curl`](https://otg.dev/clients/curl/) - The most basic utility for any kind of REST API calls, including OTG
* [`otgen`](https://otg.dev/clients/otgen/) - This command-line utility comes as part of OTG toolkit. It is capable of manipulating a wide range of OTG features while hiding a lot of complexity from a user
* [`snappi`](https://otg.dev/clients/snappi/) - Test scripts written in `snappi`, an auto-generated Python module, can be executed against any traffic generator conforming to the Open Traffic Generator API. 
* [`gosnappi`](https://otg.dev/clients/gosnappi/) - Similar to `snappi`, test scripts written in `gosnappi`, an auto-generated Go module, can be executed against any traffic generator conforming to the Open Traffic Generator API.

## Infrastructure

To manage deployment of the example labs, we use one of the following declarative tools:

* [Docker Compose](https://docs.docker.com/compose/) - general-purpose tool for defining and running multi-container Docker applications
* [Containerlab](https://containerlab.dev/) - simple yet powerful specialized tool for orchestrating and managing container-based networking labs

## CI with Github Actions

[![CI](https://github.com/open-traffic-generator/otg-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/open-traffic-generator/otg-examples/actions/workflows/ci.yml)
Most of the lab examples include Github Action workflow for executing OTG tests on any changes to the lab code. This could serve as a template for your CI workflow.

## Reference

| Lab                                                                                                                          | OTG Tool    | DUT  | Client             | Infrastructure | CI  |
| ---------------------------------------------------------------------------------------------------------------------------- | ----------- | ---- | ------------------ | -------------- | --- |
| [B2B Ixia-c Traffic](https://github.com/open-traffic-generator/otg-examples/blob/main/docker-compose/b2b)                    | Ixia-c TE   | B2B  | `otgen`            | Compose        | yes |
| [FRR Ixia-c Traffic](https://github.com/open-traffic-generator/otg-examples/blob/main/clab/ixia-c-te-frr)                    | Ixia-c TE   | FRR  | `otgen`            | Containerlab   | yes  |
| [3xB2B KENG Traffic](https://github.com/open-traffic-generator/otg-examples/blob/main/docker-compose/b2b-3pair)              | KENG TE     | B2B  | `otgen`            | Compose        | yes |
| [B2B KENG BGP and traffic](https://github.com/open-traffic-generator/otg-examples/blob/main/docker-compose/cpdp-b2b)         | KENG PE+TE  | B2B  | `gosnappi`         | Compose        | yes |
| [FRR KENG ARP, BGP and traffic](https://github.com/open-traffic-generator/otg-examples/blob/main/docker-compose/cpdp-frr)    | KENG PE+TE  | FRR  | `curl` & `otgen`   | Compose & Clab | yes |
| [Hello, snappi! Welcome to the Clab!](https://github.com/open-traffic-generator/otg-examples/blob/main/clab/ixia-c-b2b)      | Ixia-c-one  | B2B  | `snappi`           | Containerlab   | yes |
| [Dear snappi, please meet Scapy!](https://github.com/open-traffic-generator/otg-examples/blob/main/clab/ixia-c-b2b/SCAPY.md) | Ixia-c-one  | B2B  | `scapy` & `snappi` | Containerlab   | yes |
| [RTBH](https://github.com/open-traffic-generator/otg-examples/blob/main/clab/rtbh)                                           | Ixia-c-one  | FRR  | `gosnappi`         | Containerlab   | yes |


## Lab Descriptions

### [B2B Ixia-c Traffic](docker-compose/b2b)

Ixia-c traffic engine back-to-back setup with Docker Compose. Fast and easy way to get started using [`otgen`](https://github.com/open-traffic-generator/otgen) CLI tool.

### [FRR Ixia-c Traffic](clab/ixia-c-te-frr)

Ixia-c Traffic Engine and FRR. Demonstrates how to deploy Ixia-c Traffic Engine nodes in Containerlab. This setup has an FRR container as a Device Under Test.

### [3xB2B KENG Traffic](docker-compose/b2b-3pair)

KENG 3 back-to-back pairs setup with Docker Compose. This lab is an extension of [Ixia-c back-2-back lab](docker-compose/b2b/README.md) traffic engine setup with more port pairs that is allowed with free version of Ixia-c. Use this lab to validate Ixia-c commercial version – KENG for basic traffic operations.

### [B2B KENG BGP and traffic](docker-compose/cpdp-b2b)

KENG back-to-back BGP and traffic setup with Docker Compose. This is an extended version of a basic [Ixia-c back-2-back lab](docker-compose/b2b/README.md) with [Keysight Elastic Network Generator](https://www.keysight.com/us/en/products/network-test/protocol-load-test/keysight-elastic-network-generator.html) components added to emulate L2-3 protocols like BGP.

### [FRR KENG ARP, BGP and traffic](docker-compose/cpdp-frr)

KENG ARP, BGP and traffic with FRR as a DUT. This lab demonstrates validation of an FRR DUT for basic BGP peering, prefix announcements and passing of traffic between announced subnets. The lab has two alternative deployment methods: Compose as well as Containerlab.

### [Hello, snappi! Welcome to the Clab!](clab/ixia-c-b2b) 

Basics of creating a Python program to control Ixia-c-one node, all packaged in a Containerlab topology.

### [Dear snappi, please meet Scapy!](clab/ixia-c-b2b/SCAPY.md) 

Joint use of Scapy packet crafting Python module with snappi, to generate custom DNS flows via Ixia-c-one node.

### [RTBH](clab/rtbh)

Remote Triggered Black Hole (RTBH) is a common DDoS mitigation technique which uses BGP announcements to request an ISP to drop all traffic to an IP address under a DDoS attack.
