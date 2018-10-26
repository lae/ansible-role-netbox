Vagrant.configure("2") do |config|
  config.vm.box = "generic/debian9"
  config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "examples/playbook_single_host_deploy.yml"
  end
end
