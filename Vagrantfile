Vagrant.configure("2") do |config|
  config.vm.box = "generic/debian9"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "examples/playbook_single_host_deploy.yml"
  end
end
