<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void{

        Schema::create('repositories', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('owner');
            $table->string('name');
            $table->string('url');
            $table->string('branch')->default('main');
            $table->string('default_branch')->default('main');
            $table->boolean('is_watched')->default(true);
            $table->boolean('is_indexed')->default(false);
            $table->string('index_status')->default('pending');
            $table->json('metadata')->nullable();
            $table->timestamps();
        });

        Schema::create('repo_files', function (Blueprint $table) {
            $table->id();
            $table->foreignId('repository_id')->constrained()->onDelete('cascade');
            $table->string('path');
            $table->string('file_name')->nullable();
            $table->string('parent_path')->nullable();
            $table->string('extension')->nullable();
            $table->string('type');
            $table->string('sha');
            $table->unsignedInteger('size')->nullable();
            $table->boolean('is_binary')->default(false);
            $table->boolean('is_indexed')->default(false);
            $table->timestamps();
        });

        Schema::create('file_contents', function (Blueprint $table) {
            $table->id();
            $table->foreignId('repo_file_id')->constrained()->onDelete('cascade');
            $table->longText('content');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('file_contents');
        Schema::dropIfExists('repo_files');
        Schema::dropIfExists('repositories');
    }
};
