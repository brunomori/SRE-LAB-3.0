# MetalLB

O manifesto native v0.16.2 é baixado no bootstrap. A configuração `IPAddressPool` e `L2Advertisement` é gerada do pool reservado e interface real. O código instala somente depois de validar a identidade do cluster. Não ativar MetalLB também no Kubespray. A faixa deve ser reservada e fora do DHCP; o VIP da API não pertence ao pool. Consulte docs/compatibility.md.
