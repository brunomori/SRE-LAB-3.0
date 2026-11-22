# Traefik

O bootstrap baixa o chart 42.4.0, renderiza com `values.yml` e instala no namespace `traefik` usando o Helm privado. A classe `traefik` é padrão, o Service LoadBalancer recebe IP do MetalLB. HTTP local, dashboard desativado, sem Gateway API/cert-manager. O teste usa host `.test` e header Host sem alteração de DNS.
