Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"
  config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

  config.vm.provision :ansible do |ansible|
    ansible.limit = "all,localhost"
    ansible.playbook = "tests/vagrant/package_role.yml"
    ansible.verbose = true
  end

  config.vm.provision :ansible do |ansible|
    ansible.limit = "all"
    ansible.playbook = "tests/vagrant/provision.yml"
    ansible.verbose = true
  end
end
