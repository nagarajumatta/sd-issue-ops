# frozen_string_literal: true

# Add new env vars and runners to replace below
# Add new transformers for plugins if needed
env "old-env-var1", "new-env-var1"
env "old-env-var2", "new-env-var2"
env "old-env-var3", "new-env-var3"
runner "old-runner1", "new-runner1"
runner "old-runner2", "new-runner2"
runner "old-runner3", "new-runner3"

transform "jenkins.plugins.hipchat.HipChatNotifier", "org.jenkinsci.plugins.buildnamesetter.BuildNameSetter", "org.jenkinsci.plugins.builduser.BuildUser", "com.cloudbees.jenkins.GitHubSetCommitStatusBuilder", "org.jenkinsci.plugins.github.status.GitHubCommitStatusSetter", "org.jvnet.hudson.plugins.SbtPluginBuilder", "com.github.terma.jenkins.githubprcoveragestatus.CompareCoverageAction", "org.jenkinsci.plugins.github.status.GitHubCommitStatusSetter", "hudson.plugins.timestamper.TimestamperBuildWrapper", "hudson.plugins.ansicolor.AnsiColorBuildWrapper", "hudson.plugins.gradle.BuildScanBuildWrapper", "com.chikli.hudson.plugin.naginator.NaginatorPublisher", "com.cloudbees.jenkins.GitHubCommitNotifier", "hudson.plugins.descriptionsetter.DescriptionSetterPublisher", "hudson.plugins.descriptionsetter.DescriptionSetterBuilder", "org.jfrog.hudson.maven3.Maven3Builder", "org.jenkinsci.plugins.buildnameupdater.BuildNameUpdater", "hudson.plugins.testng.Publisher", "hudson.tasks.Mailer", "hudson.plugins.emailext.ExtendedEmailPublisher" do
  nil
end

# rubocop:disable Layout/HashAlignment
# rubocop:disable Layout/IndentationWidth
# rubocop:disable Layout/FirstHashElementIndentation
transform "com.cloudbees.dockerpublish.DockerBuilder" do |item|
  image_url = item["registry"]["url"]
  if image_url.is_a?(String)
    image_url = image_url.strip
    image_url = image_url.delete_prefix("https://")
  end
  repo_name = item["repoName"]
  if repo_name.is_a?(String)
    repo_name = repo_name.strip
    image_url = image_url + "/" + repo_name
  end
  if item.key?("dockerfilePath")
    dockerfile_path = item["dockerfilePath"]
    dockerfile_path = "./Dockerfile" if dockerfile_path.nil? || dockerfile_path.empty?
  else
    dockerfile_path = "./Dockerfile"
  end
  repo_tag_or_sha = item["repoTag"]
  repo_tag_or_sha = "${{ github.sha }}" if repo_tag_or_sha == "$GIT_COMMIT"
  tags_array = [repo_tag_or_sha, "latest"]
  prefixed_tags_array = tags_array.map { |element| image_url + ":" + element.to_s }
  prefixed_tags_array = prefixed_tags_array.join("\n")
  build_additional_args = item["buildAdditionalArgs"]
  if item.key?("buildContext")
    build_context = item["buildContext"]
    build_context = "." if build_context.nil? || build_context.empty?
  else
    build_context = "."
  end
  secrets = []
  build_args = []
  unless build_additional_args.nil? || build_additional_args.empty?
    build_additional_args.split.each_cons(2) do |item1, item2|
      if item1 == "--secret"
        secrets << item2
      elsif item1.start_with?("--build-arg")
        build_args << item2
      end
    end
  end
  if secrets.length == 1
    secrets = secrets[0]
  elsif secrets.length > 1
    secrets = secrets.join("\n")
  elsif secrets.length.zero?
    secrets = nil
  end
  if build_args.length == 1
    build_args = build_args[0]
  elsif build_args.length > 1
    build_args = build_args.join("\n")
  elsif build_args.length.zero?
    build_args = nil
  end
  {
    "name"          => "Build and Push Docker Image",
    "uses"          => "actions/docker-build-push-action@v4",
    "with"          => {
      "pull"        => true,
      "push"        => true,
      "tags"        => prefixed_tags_array,
      "file"        => dockerfile_path,
      "context"     => build_context,
      "secrets"     => secrets,
      "build-args"  => build_args
      }
    }
end
transform "com.michelin.cio.hudson.plugins.maskpasswords.MaskPasswordsBuildWrapper" do |item|
  secrets = {}
  unless item.nil?
    if item.key?("varPasswordPairs")
      var_password_pairs = item["varPasswordPairs"]
      unless var_password_pairs.nil?
        var_password_pairs = var_password_pairs.map { |element| element["varPasswordPair"] }
        var_password_pairs.each do |variable|
          secrets[variable["var"]] = "${{ secrets.#{variable['var']} }}"
        end
      end
    end
  end
  secrets
end
transform "EnvInjectPasswordWrapper" do |item|
  secrets = {}
  unless item.nil?
    if item.key?("passwordEntries")
      password_entries = item["passwordEntries"]
      unless password_entries.nil?
        password_entries = password_entries.map { |element| element["EnvInjectPasswordEntry"] }
        password_entries.each do |variable|
          secrets[variable["name"]] = "${{ secrets.#{variable['name']} }}"
        end
      end
    end
  end
  secrets
end
transform "org.jenkinsci.plugins.conditionalbuildstep.singlestep.SingleConditionalBuilder" do |item|
  value = {}
  condition = item["condition"]
  build_step = item["buildStep"]
  if condition["class"] == "SomeCondition1"
    if build_step["class"] == "SomeBuildStep1"
      # Do Something
    elsif build_step["class"] == "SomeBuildStep2"
      # Do Something
    else
      # Do Something
    end
  elsif condition["class"] == "SomeCondition2"
    if build_step["class"] == "SomeBuildStep1"
      # Do Something
    elsif build_step["class"] == "SomeBuildStep2"
      # Do Something
    else
      # Do Something
    end
  else
    # Do Something
  end
  value
end
transform "org.jenkinsci.plugins.conditionalbuildstep.ConditionalBuilder" do |item|
  value = {}
  condition = item["runCondition"]
  conditional_builders = item["conditionalbuilders"]
  if condition["class"] == "SomeCondition1"
    conditional_builders.each do |conditional_builder|
      if conditional_builder.key?("SomeBuildStep1")
        # Do Something
      elsif conditional_builder.key?("SomeBuildStep2")
        # Do Something
      else
        # Do Something
      end
    end
  if condition["class"] == "SomeCondition2"
    conditional_builders.each do |conditional_builder|
      if conditional_builder.key?("SomeBuildStep1")
        # Do Something
      elsif conditional_builder.key?("SomeBuildStep2")
        # Do Something
      else
        # Do Something
      end
    end
  else
    # Do Something
  end
  value
end
# rubocop:enable Layout/HashAlignment
# rubocop:enable Layout/IndentationWidth
# rubocop:enable Layout/FirstHashElementIndentation
